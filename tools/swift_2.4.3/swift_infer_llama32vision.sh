CUDA_VISIBLE_DEVICES=7 swift infer \
  --model_type llama3_2-11b-vision-instruct \
  --model_id_or_path "/home/lgd/common/ComfyUI/models/LLM/LLM-Research/Llama-3___2-11B-Vision-Instruct/"   \
  --load_dataset_config true
