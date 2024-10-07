export export CUDA_VISIBLE_DEVICES=3,4,5,6
llamafactory-cli webchat "/home/lgd/e_commerce_lmm/LLaMA-Factory-0.9.0/examples/inference/qwen2_vl.yaml"

llamafactory-cli api "/home/lgd/e_commerce_lmm/LLaMA-Factory-0.9.0/examples/inference/qwen2_vl.yaml"
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What'\''s in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }'
