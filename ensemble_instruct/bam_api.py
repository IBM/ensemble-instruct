import os
from dotenv import load_dotenv
from genai.model import Credentials, Model
from genai.schemas import GenerateParams
import json
import tqdm
import random
import argparse
import time
from datetime import datetime
from typing import List, Optional, Union
from genai.exceptions.genai_exception import GenAiException
import time

def make_bam_request(
        engine,
        api_key,
        prompts,
        decoding_method="sample",
        max_new_tokens=128,
        min_new_tokens=1,
        stream=False,
        temperature=0.7,
        top_k=50,
        top_p=1,
        stop_sequences=None):

    params = GenerateParams(
        decoding_method=decoding_method,
        max_new_tokens=max_new_tokens,
        min_new_tokens=min_new_tokens,
        stream=stream,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        stop_sequences=stop_sequences
    )
    # api_key and api_endpoint depends on the URL of the LLM host machine
    # and should be modified accordingly
    creds = Credentials(api_key, api_endpoint="https://bam-api.res.ibm.com/v1")
    chat = Model(engine, params=params, credentials=creds)

    tries = 10
    for i in range(tries): # 10 retries
        try:
            responses = chat.generate(prompts)
        except GenAiException as e:
            if i < tries -1:
                print("Timeout connection to BAM, waiting 10mins before retry")
                print(e)
                print(f"Prompts: {prompts}")
                print("Promts Lengths:")
                print([len(i.split()) for i in prompts])
                time.sleep(10*60)
                continue
            else:
                raise e
        break

    results = []
    for response in responses:
        data = {
            "prompt": response.input_text,
            "response": response.generated_text,
            "seed": response.seed,
        }
        results.append(data)

    return results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--engine",
        type=str,
        default="flan-t5-xxl",
        help="BAM model to try",
    )
    parser.add_argument(
        "--input_file",
        type=str,
        help="The input file that contains the prompts to BAM.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output file to save the responses from BAM.",
    )
    parser.add_argument(
        "--request_batch_size",
        type=int,
        default=5,
        help="The number of requests to send to BAM at a time.",
    )
    parser.add_argument(
        "--use_existing_responses",
        action="store_true",
        help="Whether to use existing responses from the output file if exists",
    )
    return parser.parse_args()

if __name__ == "__main__":
    random.seed(123)
    args = parse_args()
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    fout = open(args.output_file, "w", encoding="utf-8")
    fin = open(args.input_file, "r", encoding="utf-8")

    all_prompts = [json.loads(line)["prompt"] for line in fin]
    print(f"Loaded {len(all_prompts)} human-written seed instructions")

    # BAM_API_KEY can be set with export BAM_API_KEY=xyz either in login shell or cli
    api_key = os.getenv("BAM_API_KEY", None)

    print("\n------------- Example (GPT Chat)-------------\n")

    for i in tqdm.tqdm(range(0, len(all_prompts), args.request_batch_size)):
        batch_prompts = all_prompts[i: i + args.request_batch_size]
        responses = make_bam_request(args.engine, api_key, batch_prompts)
        for response in responses:
            fout.write(json.dumps(response) + "\n")







