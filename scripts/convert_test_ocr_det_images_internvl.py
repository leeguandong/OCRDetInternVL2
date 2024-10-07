import json
from tqdm import tqdm

def update_image_paths(input_file, output_file, new_path):
    """
    更新 JSON 文件中的 images 路径。

    :param input_file: 输入的 JSON 文件路径
    :param output_file: 输出的更新后 JSON 文件路径
    :param new_path: 新的 images 路径
    """
    # 读取 JSON 数据
    with open(input_file, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    # 更新 images 路径
    for entry in tqdm(data, desc="更新路径进度"):
        entry['images'] = new_path + entry['images'].split('/')[-1]

    # 将更新后的数据写入新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

    print("路径更新完成！")

# 使用示例
input_file = r'E:\comprehensive_library\e_commerce_lmm\data\ocr_det_test_dataset.jsonl'
output_file = r'E:\comprehensive_library\e_commerce_lmm\data\ocr_det_test_dataset_update.jsonl'
new_path = 'E:/comprehensive_library/e_commerce_lmm/data/OCR_Det/test/Images/'

update_image_paths(input_file, output_file, new_path)