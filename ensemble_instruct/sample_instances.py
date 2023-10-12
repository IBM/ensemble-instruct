import argparse
import logging
import os
import sys
import json
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

# select instruction, input and output only from machine generated instances
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")
    
    args = parser.parse_args()
    genout = open(args.outputfile, "w", encoding="utf-8")

    inputcount = 0
    instruction_list = []
    with open(args.inputfile, encoding="utf-8") as reader:
        for raw_example in reader:
            instance = json.loads(raw_example)
            instruction = instance["instruction"].strip()
            raw_instance = instance["raw_instances"].strip()
            raw_instance = raw_instance.replace("\n\n", "^")
            instances = raw_instance.split('^')
            for idx, instance in enumerate(instances):
                samples = instance.splitlines()
                # handle input-output instances
                if 'input:' in samples[0]:
                    if idx==0 and len(samples) > 1:
                        input = samples[0].strip()
                        output = samples[1].strip()
                        if 'input:' in input and 'output:' in output:
                            input = input.replace("input:","").strip()
                            input = input.replace("|EoS|","").strip()
                            output = output.replace("output:","").strip()
                            output = output.replace("|EoS|","").strip()
                            instruction = instruction.replace("|EoS|","").strip()
                            if len(output.split()) > 0 and output!="":
                                genout.write(json.dumps({
                                    "instruction": instruction,
                                    "input": input,
                                    "output": output
                                }) + "\n")
                                inputcount += 1
                    elif idx > 0 and len(samples) > 2:
                        instruction = samples[0].strip()
                        input = samples[1].strip()
                        output = samples[2].strip()
                        if 'instruction:' in instruction and 'input:' in input and \
                           'output:' in output and len(instruction.split()) > 5:
                            instruction = instruction.replace("instruction:","").strip()
                            instruction = instruction.replace("|EoS|","").strip()
                            input = input.replace("input:","").strip()
                            input = input.replace("|EoS|","").strip()
                            output = output.replace("output:","").strip()
                            output = output.replace("|EoS|","").strip()
                            if len(output.split()) > 0 and output!="":
                                genout.write(json.dumps({
                                    "instruction": instruction,
                                    "input": input,
                                    "output": output
                                }) + "\n")
                                inputcount += 1
                # handle output only instances
                elif 'output:' in samples[0] and 'input:' not in samples[0]:
                    if idx==0 and len(samples) > 0:
                        output = samples[0].strip()
                        if 'output:' in output:
                            output = output.replace("output:","").strip()
                            output = output.replace("|EoS|","").strip()
                            instruction = instruction.replace("|EoS|","").strip()
                            if len(output.split()) > 0 and output!="":
                                genout.write(json.dumps({
                                    "instruction": instruction,
                                    "input": "",
                                    "output": output
                                }) + "\n")
                                inputcount += 1
                    elif idx > 0 and len(samples) > 1:
                        instruction = samples[0].strip()
                        output = samples[1].strip()
                        if 'instruction:' in instruction and 'output:' in output and \
                           len(instruction.split()) > 5:
                            instruction = instruction.replace("instruction:","").strip()
                            instruction = instruction.replace("|EoS|","").strip()
                            output = output.replace("output:","").strip()
                            output = output.replace("|EoS|","").strip()
                            if len(output.split()) > 0 and output != "":
                                genout.write(json.dumps({
                                    "instruction": instruction,
                                    "input": "",
                                    "output": output
                                }) + "\n")
                                inputcount += 1
                               
    print("good_instruction:", inputcount)

if __name__ == "__main__":
    main()

    
    
