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
        "--engine",
        type=str,
        default="google/flan-t5-xxl",
        help="The LLM engine for output generation"
    )
    parser.add_argument(
        "--request_batch_size",
        type=int,
        default=5,
        help="The number of requests to send in a batch."
    )
    parser.add_argument(
        "--num_instructions",
        type=int,
    )
    parser.add_argument(
        "--input_file",
        required=True,
        type=str,
        help="input_generated_instances.jsonl",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="zeroshot output_generated.jsonl",
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    api_key = os.getenv("BAM_API_KEY", None)

    # read input file up to the specified number of instructions
    with open(os.path.join(args.batch_dir, args.input_file)) as fin:
        lines = fin.readlines()
        if args.num_instructions is not None:
            lines = lines[:args.num_instructions]

    # read previously generated output file and store the samples in existing_requests
    output_path = os.path.join(args.batch_dir, args.output_file)
    existing_requests = {}
    if os.path.exists(output_path):
        with open(output_path) as fin:
            for line in tqdm.tqdm(fin):
                try:
                    data = json.loads(line)
                    existing_requests[data["instruction"]] = data
                except:
                    pass
        print(f"Loaded {len(existing_requests)} existing requests")

    progress_bar = tqdm.tqdm(total=len(lines))
    with open(output_path, "w") as fout:
        for batch_idx in range(0, len(lines), args.request_batch_size):
            batch = [json.loads(line) for line in lines[batch_idx: batch_idx + args.request_batch_size]]
            if all(d["instruction"] in existing_requests for d in batch):
                for d in batch:
                    data = existing_requests[d["instruction"]]
                    data = OrderedDict(
                        (k, data[k]) for k in \
                            ["instruction", "input", "output"]
                        )
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
            else:
                prompts = [d["instruction"].strip() + "\n" + d["input"].strip() for d in batch]
                results = make_bam_request(
                    args.engine,
                    api_key,
                    prompts,
                    decoding_method="greedy",
                    max_new_tokens=256,
                    min_new_tokens=1,
                    stop_sequences=["\n\n","|EoS|"]
                )

                for i in range(len(batch)):
                    data = batch[i]
                    if results[i]["response"] is not None:
                        data["output"] = results[i]["response"]
                    else:
                        data["output"] = ""
                    data = {
                        "instruction": data["instruction"],
                        "input": data["input"],
                        "output": data["output"]
                    }
                    data = OrderedDict(
                        (k, data[k]) for k in \
                            ["instruction", "input", "output"]
                        )
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
            progress_bar.update(len(batch))
