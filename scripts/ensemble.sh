batch_dir=sample/
prefix="openei"

python ensemble_instruct/ensemble_output.py \
       --genoutput1 $batch_dir/$prefix.flan-t5-xxl_output.jsonl \
       --genoutput2 $batch_dir/$prefix.flan-ul2_output.jsonl \
       --instance_file $batch_dir/$prefix.samples.jsonl \
       --ensemble $batch_dir/$prefix.ensemble
