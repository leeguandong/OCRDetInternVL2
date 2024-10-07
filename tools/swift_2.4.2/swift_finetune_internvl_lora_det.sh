NPROC_PER_NODE=4 CUDA_VISIBLE_DEVICES=4,5,6,7 swift sft \
  --model_type internvl2-8b \
  --model_id_or_path /home/lgd/common/ComfyUI/models/LLM/opengvlab/internvl2-8b/   \
  --dataset "/home/lgd/e_commerce_lmm/data/ocr_det_train_dataset.jsonl" \
  --lora_target_modules ALL \
  --lora_lr_ratio 16.0 \
  --lora_rank 16 \
  --learning_rate 1e-4 \
  --num_train_epochs 5 \
  --use_flash_attn True \
  --gradient_accumulation_steps 4 \
  --batch_size 2 \
  --eval_steps 1000 \
  --save_steps 500 \
  --neftune_noise_alpha 5 \
  --output_dir /home/lgd/e_commerce_lmm/results/internvl2_swift_ocrdet/  \
  --logging_dir /home/lgd/e_commerce_lmm/results/internvl2_swift_ocrdet/
  #  --device_max_memory 15GB 15GB 15GB 15GB \