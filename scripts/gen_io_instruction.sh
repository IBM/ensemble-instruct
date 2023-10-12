batch_dir=debug

python ensemble_instruct/gen_instructions.py \
    --batch_dir ${batch_dir} \
    --num_instructions_to_generate 50 \
    --seed_tasks_path data/seed_tasks.jsonl \
    --num_prompt_instructions 24 \
    --instruction_type input_output \
    --request_batch_size 5 \
    --outputfile falcon40b_io_instructions.jsonl \
    --engine tiiuae/falcon-40b


