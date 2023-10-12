batch_dir=sample/
prefix="openei"

echo "Generating instructions that require input-output instances"
python ensemble_instruct/gen_instructions.py \
    --batch_dir ${batch_dir} \
    --num_instructions_to_generate 100 \
    --seed_tasks_path data/seed_tasks.jsonl \
    --num_prompt_instructions 24 \
    --instruction_type input_output \
    --request_batch_size 5 \
    --outputfile $prefix.io_instructions.jsonl \
    --engine tiiuae/falcon-40b

echo "Generating instrucitons that require output only instances"
python ensemble_instruct/gen_instructions.py \
    --batch_dir ${batch_dir} \
    --num_instructions_to_generate 100 \
    --seed_tasks_path data/seed_tasks.jsonl \
    --num_prompt_instructions 10 \
    --instruction_type output \
    --request_batch_size 5 \
    --outputfile $prefix.o_instructions.jsonl \
    --engine tiiuae/falcon-40b

echo "Generating input-output instances"
python ensemble_instruct/gen_instances.py \
    --batch_dir ${batch_dir} \
    --input_file $prefix.io_instructions.jsonl \
    --output_file $prefix.io_instances.jsonl \
    --template input_output \
    --request_batch_size 5 \
    --engine tiiuae/falcon-40b

echo "Generating output only instances"
python ensemble_instruct/gen_instances.py \
    --batch_dir ${batch_dir} \
    --input_file $prefix.o_instructions.jsonl \
    --output_file $prefix.o_instances.jsonl \
    --template output \
    --request_batch_size 5 \
    --engine tiiuae/falcon-40b

echo "Select valid input-output instances"
python ensemble_instruct/sample_instances.py $batch_dir/$prefix.io_instances.jsonl $batch_dir/$prefix.io_samples.jsonl

echo "Select valid output only instances"
python ensemble_instruct/sample_instances.py $batch_dir/$prefix.o_instances.jsonl $batch_dir/$prefix.o_samples.jsonl

echo "merge input-output instances with output only instances"
cp $batch_dir/$prefix.io_samples.jsonl $batch_dir/$prefix.samples.jsonl
cat $batch_dir/$prefix.o_samples.jsonl >> $batch_dir/$prefix.samples.jsonl

echo "generate flan-t5-xxx output given instruction and input"
python ensemble_instruct/gen_output_zeroshot.py \
    --batch_dir ${batch_dir} \
    --input_file $prefix.samples.jsonl \
    --output_file $prefix.flan-t5-xxl_output.jsonl \
    --request_batch_size 5 \
    --engine google/flan-t5-xxl

echo "generate flan-ul2 output given instruction and input"
python ensemble_instruct/gen_output_zeroshot.py \
    --batch_dir ${batch_dir} \
    --input_file $prefix.samples.jsonl \
    --output_file $prefix.flan-ul2_output.jsonl \
    --request_batch_size 5 \
    --engine google/flan-ul2

echo "generate ensembled output given instruction and input"
python ensemble_instruct/ensemble_output.py \
       --genoutput1 $batch_dir/$prefix.flan-t5-xxl_output.jsonl \
       --genoutput2 $batch_dir/$prefix.flan-ul2_output.jsonl \
       --instance_file $batch_dir/$prefix.samples.jsonl \
       --ensemble $batch_dir/$prefix.ensemble
