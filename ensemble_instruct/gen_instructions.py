import os
import json
import random
import re
import string
import tqdm
import argparse
import numpy as np
import pandas as pd
from multiprocessing import Pool
from functools import partial
from rouge_score import rouge_scorer
from bam_api import make_bam_request
from dotenv import load_dotenv
from genai.model import Credentials, Model
from genai.schemas import GenerateParams

random.seed(42)

def encode_prompt(prompt_instructions):
    """Encode multiple prompt instructions into a single string."""
    prompt = "Come up with a series of tasks:\n"
    for idx, instruction in enumerate(prompt_instructions):
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        prompt += f"{idx+1}. {instruction} |EoS|\n"
    prompt += f"{len(prompt_instructions) + 1}."
    return prompt

def sample_machine_instructions(machine_instructions, similarities, n):
    """Sample n machine instructions from a list of machine instructions."""
    return random.sample(machine_instructions, min(n, len(machine_instructions)))

def find_word_in_string(w, s):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search(s)

def post_process_bam_response(response):
    if response is None:
        return []
    raw_instructions = re.split(r"\n\d+\s?\. ", response)
    instructions = []
    for inst in raw_instructions:
        inst = re.sub(r"\s+", " ", inst).strip()
        if inst == "":
            continue
        # filter out too short or too long instructions
        if len(inst.split()) <= 3 or len(inst.split()) > 150:
            continue
        # filter based on keywords that are not suitable for language models.
        if any(find_word_in_string(word, inst) for word in ["image", "images", "graph", "graphs", "picture", "pictures", "file", "files", "map", "maps", "draw", "plot", "go to"]):
            continue
        # Note this is not a comprehensive filtering for all programming instructions.
        if inst.startswith("Write a program"):
            continue
        # filter those starting with punctuation
        if inst[0] in string.punctuation:
            continue
        # filter those starting with non-english character
        if not inst[0].isascii():
            continue
        instructions.append(inst)
    return instructions

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch_dir",
        type=str,
        required=True,
        default="data/bloom/",
        help="The directory where the batch is stored.",
    )
    parser.add_argument(
        "--seed_tasks_path",
        type=str,
        required=True,
        default="data/seed_tasks.jsonl",
        help="The path to the human written data.",
    )
    parser.add_argument(
        "--instruction_type",
        type=str,
        required=True,
        help="instance type for instruction: output for output only input_output for input-output",
    )
    parser.add_argument(
        "--engine",
        type=str,
        default="tiiuae/falcon-40b",
        help="LLM engine to call for data generation"
    )
    parser.add_argument(
        "--num_prompt_instructions",
        type=int,
        default=24,
        help="number of ICL samples: 24 for input-output instance and 10 for output-only instances"
    )
    parser.add_argument(
        "--num_instructions_to_generate",
        type=int,
        default=100,
        help="number of instructions to be generated",
    )
    parser.add_argument(
        "--request_batch_size",
        type=int,
        default=5,
        help="number of requests to be sent at a time."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        default="io_instructions.jsonl"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    seed_tasks = [json.loads(l) for l in open(args.seed_tasks_path, "r")]
    seed_instructions = []

    # if the instruction type == input-output, read instructions with input-output instance
    # if the instruction type == output, read instructions with output only instance
    for t in seed_tasks:
        instance = t["instances"][0]
        if args.instruction_type=="input_output":
            if instance["input"]!="":
                seed_instructions.append(t["instruction"])
        elif args.instruction_type=="output":
            if instance["input"]=="":
                seed_instructions.append(t["instruction"])
                
    print(f"Loaded {len(seed_instructions)} human-written seed instructions")
    
    # make sure BAM_API_KEY is set as an environment variable 
    api_key = os.getenv("BAM_API_KEY", None)
    
    os.makedirs(args.batch_dir, exist_ok=True)
    request_idx = 0
    
    # load previously generated instructions by LLM
    machine_instructions = []
    if os.path.exists(os.path.join(args.batch_dir, args.outputfile)):
        with open(os.path.join(args.batch_dir, args.outputfile), "r") as fin:
            for line in fin:
                instruction_info = json.loads(line)
                machine_instructions.append(instruction_info["instruction"])
                request_idx = instruction_info["request_idx"] + 1
        print(f"Loaded {len(machine_instructions)} input-generated instructions")

    # similarities = {}
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    
    # generate new instructions!
    progress_bar = tqdm.tqdm(total=args.num_instructions_to_generate)
    if machine_instructions:
        progress_bar.update(len(machine_instructions))

    with open(os.path.join(args.batch_dir, args.outputfile), "a") as fout:
        while len(machine_instructions) < args.num_instructions_to_generate:
            batch_inputs = []
            # Prepare for the prompts with ICL samples
            for _ in range(args.request_batch_size):
                # select maximum of 4 instructions (out of 24 or 10) from machine generated ones
                prompt_instructions = sample_machine_instructions(
                    machine_instructions, 
                    similarities=None,
                    n=4)
                # sample human instructions from the pool
                prompt_instructions += random.sample(seed_instructions, args.num_prompt_instructions - len(prompt_instructions))
                random.shuffle(prompt_instructions)
                prompt = encode_prompt(prompt_instructions)
                batch_inputs.append(prompt)
                
            # send the prompts to the LLM for new instructions
            results = make_bam_request(
                args.engine,
                api_key,
                batch_inputs,
                decoding_method="sample",
                max_new_tokens=256,
                min_new_tokens=15,
                stop_sequences=["|EoS|"]
            )

            instructions = []
            all_metadata = []
            for result in results:
                new_instructions = post_process_bam_response(result["response"])
                instructions += new_instructions
                all_metadata += [result] * len(new_instructions)

            # similarity score computation from https://github.com/yizhongw/self-instruct
            for inst, metadata in zip(instructions, all_metadata):
                with Pool(4) as p:
                    rouge_scores = p.map(partial(scorer.score, inst), seed_instructions + machine_instructions)
                rouge_scores = [score["rougeL"].fmeasure for score in rouge_scores]
                if max(rouge_scores) > 0.7:
                    continue
                all_instructions = seed_instructions + machine_instructions
                most_similar_instructions = {
                        all_instructions[i] : rouge_scores[i] for i in np.argsort(rouge_scores)[-10:][::-1]
                    }
                machine_instructions.append(inst)
                fout.write(json.dumps({
                    "instruction": inst,
                    "most_similar": most_similar_instructions,
                    "avg_similarity_score": float(np.mean(rouge_scores)),
                    "metadata": metadata,
                    "request_idx": request_idx
                }) + "\n")
                progress_bar.update(1)
            request_idx += 1
