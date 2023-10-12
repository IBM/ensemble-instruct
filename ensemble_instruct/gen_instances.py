import os
import json
import random
import tqdm
import re
import argparse
import pandas as pd
from collections import OrderedDict
from bam_api import make_bam_request
from dotenv import load_dotenv
from genai.model import Credentials, Model
from genai.schemas import GenerateParams
from templates.instance_template import output_template, input_output_template

random.seed(42)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch_dir",
        type=str,
        required=True,
        help="The directory where the batch is stored.",
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        default="machine_generated_instructions.jsonl",
        help="machine generated instruction file",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        default="machine_generated_instances.jsonl",
        help="machine generated instance output file",
    )
    parser.add_argument(
        "--num_instructions",
        type=int,
        help="if specified, only generate instance input for this many instructions",
    )
    parser.add_argument(
        "--max_instances_to_generate",
        type=int,
        default=1,
        help="The max number of instances to generate for each instruction.",
    )
    parser.add_argument(
        "--template",
        type=str,
        default="input_output",
        help="Which template to use: output_template or input_output_template",
    )
    parser.add_argument(
        "--engine",
        type=str,
        default="tiiuae/falcon-40b",
        help="The engine to use."
    )
    parser.add_argument(
        "--request_batch_size",
        type=int,
        default=5,
        help="The number of requests to send in a batch."
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    api_key = os.getenv("BAM_API_KEY", None)
    # read the input file containing machine instructions
    with open(os.path.join(args.batch_dir, args.input_file)) as fin:
        lines = fin.readlines()
        if args.num_instructions is not None:
            lines = lines[:args.num_instructions]
        tasks = []
        for line in lines:
            data = json.loads(line)
            if "metadata" in data:
                data["instruction_metadata"] = data["metadata"]
                del data["metadata"]
            tasks.append(data)

    output_path = os.path.join(args.batch_dir, args.output_file)
    existing_requests = {}
    # check to see if an output file already exists
    # if the output file exists, read the previously generated outputs
    if os.path.exists(output_path):
        with open(output_path) as fin:
            for line in tqdm.tqdm(fin):
                try:
                    data = json.loads(line)
                    existing_requests[data["instruction"]] = data
                except:
                    pass
        print(f"Loaded {len(existing_requests)} existing requests")

    progress_bar = tqdm.tqdm(total=len(tasks))
    with open(output_path, "w") as fout:
        for batch_idx in range(0, len(tasks), args.request_batch_size):
            batch = tasks[batch_idx: batch_idx + args.request_batch_size]
            if all(d["instruction"] in existing_requests for d in batch):
                for d in batch:
                    data = existing_requests[d["instruction"]]
                    data = OrderedDict(
                        (k, data[k]) for k in \
                            ["instruction", "raw_instances"]
                        )
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
            else:
                prompts = []
                for task in batch:
                    # if output instance only, read output_template
                    # otherwise, read input_output_template
                    if args.template == "output":
                        prompt = output_template + " " + task["instruction"].strip() + "\n"
                    elif args.template == "input_output":
                        prompt = input_output_template + " " + task["instruction"].strip() + "\n"
                    prompts.append(prompt)
                    
                results = make_bam_request(
                    args.engine,
                    api_key,
                    prompts,
                    decoding_method="sample",
                    max_new_tokens=512,
                    min_new_tokens=50,
                    stop_sequences=["\n\n", "|EoS|"]
                )
                for i in range(len(batch)):
                    data = batch[i]
                    data["instance_metadata"] = results[i]
                    if results[i]["response"] is not None:
                        data["raw_instances"] = results[i]["response"]
                    else:
                        data["raw_instances"] = ""
                    data = OrderedDict(
                        (k, data[k]) for k in \
                            ["instruction", "raw_instances"]
                        )
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
            progress_bar.update(len(batch))
