# fine-tuning LLM & projector, freeze vision encoder
NPROC_PER_NODE=4 CUDA_VISIBLE_DEVICES=4,5,6,7 swift sft \
  --model_type llama3_2-11b-vision-instruct \
  --model_id_or_path "/home/lgd/common/ComfyUI/models/LLM/LLM-Research/Llama-3___2-11B-Vision-Instruct/"   \
  --dataset "/home/lgd/e_commerce_lmm/data/XrayGLM/open-zh-swift-llama32vision-prompt.json" \
  --sft_type lora \
  --output_dir /home/lgd/e_commerce_lmm/results/llama32vision_swift_xray/ \
  --num_train_epochs 10 \
  --max_length 2048 \
  --gradient_checkpointing true \
  --batch_size 8 \
  --gradient_accumulation_steps 4 \
  --eval_steps 1000 \
  --save_steps 500 \
  --save_total_limit 10 \
  --logging_steps 10 \
