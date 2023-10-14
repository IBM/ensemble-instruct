import argparse
import logging
import os
import sys
import json
import re
from collections import defaultdict
from rouge_score import rouge_scorer
from multiprocessing import Pool
import string

#set_progress_bar_enabled(False)
logger = logging.getLogger(__name__)

def normalize_answer(s):
    """Lower text and remove punctuation, and extra whitespace."""
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_punc(lower(s)))

def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))

def rouge1_score(prediction, ground_truth):
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(prediction=prediction, target=ground_truth)
    return scores["rouge1"].fmeasure

def rougeL_score(prediction, ground_truth):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(prediction=prediction, target=ground_truth)
    return scores["rougeL"].fmeasure

def read_output_jsonfile(file_name):
    output_list = []
    with open(file_name, encoding="utf-8") as reader:
        for line in reader:
            instance = json.loads(line)
            classlabel = instance["output"].strip()
            output_list.append(classlabel)
    return output_list

def compute_EM(instance_output, output1, output2):
    io_o1 = exact_match_score(instance_output, output1)
    io_o2 = exact_match_score(instance_output, output2)
    o1_o2 = exact_match_score(output1, output2)
    return io_o1, io_o2, o1_o2

def compute_rougeL(instance_output, output1, output2):
    io_o1_R = rougeL_score(instance_output, output1)
    io_o2_R = rougeL_score(instance_output, output2)
    o1_o2_R = rougeL_score(output1, output2)
    return io_o1_R, io_o2_R, o1_o2_R

def select_worst_rougescore(io_o1_R, io_o2_R, o1_o2_R):
    if io_o1_R <= io_o2_R and io_o1_R <= o1_o2_R:
        return io_o1_R
    elif io_o2_R <= io_o1_R and io_o2_R <= o1_o2_R:
        return io_o2_R
    elif o1_o2_R <= io_o1_R and o1_o2_R <= io_o2_R:
        return o1_o2_R

def select_best_rouge(io_o1_R, io_o2_R, o1_o2_R, instance_output, output1, output2):
    score1 = io_o1_R + io_o2_R
    score2 = io_o1_R + o1_o2_R
    score3 = io_o2_R + o1_o2_R
    
    if score1 >= score2 and score1 >= score3:
        return score1, instance_output
    elif score2 >= score1 and score2 >= score3:
        return score2, output1
    elif score3 >= score1 and score3 >= score2:
        return score3, output2

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--genoutput1",
        type=str,
        required=True,
        help="generated output file1 zeroshot"
    )
    parser.add_argument(
        "--genoutput2",
        type=str,
        required=True,
        help="generated output file2 zeroshot"
    )
    parser.add_argument(
        "--instance_file",
        type=str,
        required=True,
        help="instruction-instance file used for output generation"
    )
    parser.add_argument(
        "--ensemble",
        type=str,
        required=True,
        help="ensembed instance file via output ensembling"
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    genoutput1 = read_output_jsonfile(args.genoutput1)
    genoutput2 = read_output_jsonfile(args.genoutput2)

    if len(genoutput1) != len(genoutput2):
        raise Exception("Sorry, len(genoutput1) and len(genoutput2) are not the same!")
    ensemble = open(args.ensemble, "w", encoding="utf-8")
    
    linecount = 0
    with open(args.instance_file, encoding="utf-8") as reader:
        for line in reader:
            instance = json.loads(line)
            instruction = instance["instruction"].strip()
            input = instance["input"].strip()
            instance_output = instance["output"].strip()
            output1 = genoutput1[linecount]
            output2 = genoutput2[linecount]

            instance_output_norm = normalize_answer(instance_output)
            output1_norm = normalize_answer(output1)
            output2_norm = normalize_answer(output2)

            io_o1, io_o2, o1_o2 = compute_EM(instance_output_norm, output1_norm, output2_norm)
            io_o1_R, io_o2_R, o1_o2_R = compute_rougeL(instance_output_norm, output1_norm, output2_norm)

            # greedy selection of EM output
            em_flag = 0
            if io_o1==1 or io_o2==1:
                ensemble.write(json.dumps({
                    "instruction": instruction,
                    "input": input,
                    "output": instance_output
                }) + "\n")
                em_flag = 1
            elif em_flag==0 and o1_o2==1:
                ensemble.write(json.dumps({
                    "instruction": instruction,
                    "input": input,
                    "output": instance_output
                }) + "\n")
                em_flag = 1
                
            worst_rouge_score = select_worst_rougescore(io_o1_R, io_o2_R, o1_o2_R)
            best_rouge_score, best_output = select_best_rouge(io_o1_R, io_o2_R, o1_o2_R, instance_output, output1, output2)
            
            # Select only the best output with the minimum rougeL agreement score
            if em_flag==0 and worst_rouge_score > 0.01 and best_output!="":
                ensemble.write(json.dumps({
                    "instruction": instruction,
                    "input": input,
                    "output": best_output
                }) + "\n")
            
            linecount += 1
    print("linecount: ", linecount)


    
    
