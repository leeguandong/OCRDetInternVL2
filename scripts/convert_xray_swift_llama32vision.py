import json
from tqdm import tqdm

import json
from tqdm import tqdm


def update_image_paths(input_json_file, output_json_file, new_path):
    """
    更新JSON文件中的images路径并输出到新的JSON文件

    :param input_json_file: 输入的JSON文件路径
    :param output_json_file: 输出的新的JSON文件路径
    :param new_path: 新的图片路径
    """
    # 读取输入的JSON文件
    with open(input_json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 修改数据中的images路径
    for item in tqdm(data, desc="更新路径进度"):
        item['images'] = [new_path + img.split('/')[-1] for img in item['images']]

    # 将修改后的数据写入到新的JSON文件
    with open(output_json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 使用示例
update_image_paths(r'E:\comprehensive_library\e_commerce_lmm\data\open-zh-swift-llava-prompt.json',
                   r'E:\comprehensive_library\e_commerce_lmm\data\open-zh-swift-llama32vision-prompt.json',
                   '/home/lgd/e_commerce_lmm/data/XrayGLM/images2/')
