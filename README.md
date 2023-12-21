# ensemble-instruct

This repo includes the codebase release for the following EMNLP2023 paper:

**[Ensemble-Instruct: Instruction Tuning Data Generation with a Heterogeneous Mixture of LMs](https://aclanthology.org/2023.findings-emnlp.836)**

We also release the synthetic dataset ***data/ensemble-instruct.jsonl*** under apache-2.0 license.

### Installation

1. git clone https://github.com/IBM/ensemble-instruct 
2. cd ensemble-instruct 
3. Create a conda environment of your choice. Once such example would look like:
   
   conda create -y -p ./eienvs python=3.11
   
4. Activate the conda environment 
   conda activate ./eienvs 
5. Install the dependencies using the following command: 
   pip install -r requirements.txt

### Environment Variable

This repo assumes that all of the LLM's are accessible from the
following platform, which requires an access key:

https://bam.res.ibm.com/

And the access key can be set using the following command in your login shell:
export BAM_API_KEY=xyz

All of the models used in our experiments can also be accessed from:
huggingface models: https://huggingface.co/models

And you need to set the BAM_API_KEY to the access key of the platform of your choice

### Ensemble Instruct

Step 0: In the repo directory, create a subdirectory sample, as shown below

mkdir sample

**Synthetic intruction tuning data set acquisition comprises 5 steps**:

**Step 1: Instruction generation**
Instructions are divided into 2 categories:

1. Instruction that requires input-output instances, which can be obtained with:
   scripts/gen_io_instruction.sh
2. Instruction that require output only instances, which can be obtained with:
   scripts/gen_o_instruction.sh

**Step 2: Instance generation**

Instances are also divided into 2 categories:

1. Input-output instances, which can be obtained with:
   scripts/gen_io_instance.sh
2. Output only instances, which can be obtained with:
   scripts/gen_o_instance.sh

**Step 3: Filtering out invalid instances**

Not all of the generated instances are in valid format. So we select only valid instances
with the script ensemble_instruct/sample_instances.py input output

Input-output instances and output only instances can be merged at this stage to
proceed with output generation in the next step.

**Step 4: Additional output generation**

For output ensemble, we generate addition outputs given the instruction and (optional) input obtained in Steps 1 & 2, using flan-t5-xxl and flan-ul2 as follows:

1. Output generation with flan-t5-xxl
   scripts/gen_output_flan-t5-xxl.sh
2. Output generation with flan-ul2
   scripts/gen_output_flan-ul2.sh

**Step 5: Ensemble Instruct**

We apply ensembling of 3 sets ouf outputs generated in Step 2 and Step 4 to select high
quality output as the final output, which can be obtained with

scripts/ensemble.sh

### Putting all things together

The following script run all of the 5 steps in one pipeline:

scripts/ensemble_instruct.sh

All of the intermediate outputs can be found in the directory:
sample/

The final ensembled output is: **sample/openei.ensemble**

### Citation

@inproceedings{ensemble-instruct2023, \
  title={Ensemble-Instruct: Instruction Tuning Data Generation with a Heterogeneous Mixture of LMs},\
  author={Lee, Young-Suk and Sultan, Arafat and El-Kurdi, Yousef and Naseem, Tahira and Munawar, Asim and Florian, Radu and Roukos, Salim and Astudillo, Ramon}, \
  journal={Findings of the Association for Computational Linguistics: EMNLP 2023}, \
  pages={12561-12571},
  year={2023}
}

### Acknowledgement

**gen_instruction.py** and **gen_instances.py** are adapted from [bootstrap_instruction](https://github.com/yizhongw/self-instruct/blob/main/self_instruct/bootstrap_instructions.py)
and [generate_instances](https://github.com/yizhongw/self-instruct/blob/main/self_instruct/generate_instances.py) respectively. **seed_tasks.jsonl** is an exact copy of [seed_tasks](https://github.com/yizhongw/self-instruct/blob/main/data/seed_tasks.jsonl)
