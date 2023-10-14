# ensemble-instruct

This repo includes the codebase release for the following EMNLP2023 paper:

Ensemble-Instruct: Generating Instruction-Tuning Data with a Heterogeneous Mixture of LMs

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

1. watsonx.ai: https://www.ibm.com/products/watsonx-ai or
2. huggingface models: https://huggingface.co/models

And you need to set the BAM_API_KEY to the access key of the platform of your choice

### Ensemble Instruct



