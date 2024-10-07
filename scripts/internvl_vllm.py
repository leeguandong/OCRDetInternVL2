import os
import json
import time
from datetime import datetime
from vllm import LLM, SamplingParams
from PIL import Image
import re

os.environ['CUDA_VISIBLE_DEVICES'] = '7'  # 指定使用第 7 块 GPU

class ImageOCR:
    def __init__(self, model_path, image_path):
        self.model_path = model_path
        self.image_path = image_path
        self.llm = LLM(
            model=self.model_path,
            max_model_len=3072,
            dtype='float16',
            trust_remote_code=True,
            max_num_seqs=5,
        )
        self.template = "<|im_start|>User\n{prompt}<|im_end|>\n<|im_start|>Assistant\n"
        self.prompt = "<image>\n简单描述一下图中产品,不要用中文回答，记住描述不需要复杂，如下所示：pale golden rod circle with old lace background \n"
        self.prompt = self.template.format(prompt=self.prompt)
        self.sampling_params = SamplingParams(
            temperature=0.3,
            repetition_penalty=1.05,
            max_tokens=2048,
            stop='<|end|>'
        )

    def infer_image(self, image):
        outputs = self.llm.generate(
            {
                "prompt": self.prompt,
                "multi_modal_data": {
                    "image": image
                }
            },
            sampling_params=self.sampling_params
        )
        generated_text = outputs[0].outputs[0].text
        # 使用正则表达式过滤掉中文
        filtered_text = re.sub(r'[\u4e00-\u9fa5]+', '', generated_text)
        return filtered_text

    def save_to_jsonl(self, save_file):
        st = time.time()
        with open(save_file, 'w') as f_writer:
            for root, dirs, files in os.walk(self.image_path):
                for file in files:
                    if not file.endswith(('.jpg', 'png')):
                        continue
                    image_file = os.path.join(root, file)
                    try:
                        print(image_file)
                        image = Image.open(image_file)
                        ocr_text = self.infer_image(image)
                        print(ocr_text)
                        data = {
                            "text": ocr_text,
                            "image": image_file,
                            # "conditioning_image": image_file  # 根据实际情况修改
                        }
                        json.dump(data, f_writer)
                        f_writer.write('\n')
                    except:
                        continue
        print(f"time used: {time.time() - st}")

if __name__ == "__main__":
    model_path = "/home/lgd/common/ComfyUI/models/LLM/InternVL2-2B/"
    image_path = "/home/lgd/e_commerce_sd/data/datasets/GdsSegDataSets/test_423/image/"
    ocr = ImageOCR(model_path, image_path)
    save_file = f"image_ocr_{datetime.now().strftime('%Y%m%d%H%M%S')}.jsonl"
    ocr.save_to_jsonl(save_file)