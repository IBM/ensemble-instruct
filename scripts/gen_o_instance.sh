batch_dir=debug

python ensemble_instruct/gen_instances.py \
    --batch_dir ${batch_dir} \
    --input_file falcon40b_o_instructions.jsonl \
    --output_file falcon40b_o_instances.jsonl \
    --template output \
    --request_batch_size 5 \
    --engine tiiuae/falcon-40b


