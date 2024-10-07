import json
import base64
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY', base_url='http://118.25.178.140:11246/v1')
model_name = client.models.list().data[0].id


# 图片转base64函数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 原图片转base64
def get_response(input_image_path):
    base64_image = encode_image(input_image_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": '''职位：你是一个面向证书图像的目标检测大师，具备精准识别、定位图像中相应位置的能力。
        职能：从各类卡证和票据等图像中检测到证书编码区域并给出边界框。
        **注意**：仅以给定格式返回检测结果，不要给出其它任何解释。
        **注意**：若图片中没有典型场景，返回<ref> class_name </ref><box>[[0, 0, 0, 0]]</box>即可。
        '''
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '请目标检测图像中的相应位置并给出边界框'
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            # "url": 'https://i-blog.csdnimg.cn/direct/253ad27104b7466792511f78e9f636a9.png'
                        }
                    },
                ]
            }
        ],
        temperature=0.8,
        top_p=0.8)
    return response.choices[0].message.content


def read_jsonl(file_path):
    """
    Read a JSONL file and return a list of dictionaries.

    :param file_path: Absolute path of the JSONL file to be read.
    :return: List of dictionaries representing the JSON objects in the file.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data


data = read_jsonl(r'E:\comprehensive_library\e_commerce_lmm\data\ocr_det_test_dataset_update.jsonl')

result = []
for single_data in tqdm(data):
    img_path = single_data['images']
    single_result = get_response(img_path)
    print(single_result)
    result.append({'images': img_path, 'response': single_result})

pd.DataFrame(result).to_excel('llm_response.xlsx', index=False)
