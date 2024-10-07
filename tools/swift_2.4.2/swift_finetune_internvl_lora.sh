# Experimental environment: 3090
# 23GB GPU memory
NPROC_PER_NODE=4 CUDA_VISIBLE_DEVICES=4,5,6,7 swift sft \
  --model_type internvl2-8b \
  --model_id_or_path /home/lgd/common/ComfyUI/models/LLM/opengvlab/internvl2-8b/   \
  --dataset "/home/lgd/e_commerce_lmm/data/ESTVQA_cn_rectw17_ocr_swift.jsonl" \
  --sft_type lora \
  --tuner_backend peft \
  --template_type internvl2 \
  --dtype AUTO \
  --output_dir /home/lgd/e_commerce_lmm/results/internvl2_swift_ocr/ \
  --num_train_epochs 10 \
  --max_length 2048 \
  --check_dataset_strategy warning \
  --lora_rank 8 \
  --lora_alpha 32 \
  --lora_dropout_p 0.05 \
  --lora_target_modules ALL \
  --gradient_checkpointing true \
  --batch_size 2 \
  --weight_decay 0.1 \
  --learning_rate 1e-4 \
  --gradient_accumulation_steps 8 \
  --max_grad_norm 0.5 \
  --warmup_ratio 0.03 \
  --eval_steps 1000 \
  --save_steps 500 \
  --save_total_limit 10 \
  --logging_steps 10 \
  --use_flash_attn false
  #--deepspeed default-zero2
