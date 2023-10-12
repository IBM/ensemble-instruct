batch_dir=debug
python ensemble_instruct/gen_output_zeroshot.py \
    --batch_dir ${batch_dir} \
    --input_file o_instances.jsonl \
    --output_file flan-t5-xxl_o_output.jsonl \
    --request_batch_size 5 \
    --engine google/flan-t5-xxl


