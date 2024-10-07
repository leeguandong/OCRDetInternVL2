import os
import shutil
import random
from tqdm import tqdm

import os
import shutil
import random
from tqdm import tqdm


def split_dataset(annotations_dir, images_dir, train_dir, test_dir, split_ratio=0.9):
    # 创建训练和测试文件夹
    os.makedirs(os.path.join(train_dir, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(train_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'images'), exist_ok=True)

    # 获取所有XML文件和图片文件
    xml_files = [f for f in os.listdir(annotations_dir) if f.endswith('.xml')]
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

    matched_files = []
    unmatched_files = []

    # 匹配文件名
    for xml_file in tqdm(xml_files, desc="匹配文件"):
        base_name = os.path.splitext(xml_file)[0]
        corresponding_image = f"{base_name}.jpg"  # 假设图片为jpg格式

        if corresponding_image in image_files:
            matched_files.append((xml_file, corresponding_image))
        else:
            unmatched_files.append(xml_file)

    # 打印未匹配的XML文件名
    if unmatched_files:
        print("未匹配的XML文件名:")
        for unmatched in unmatched_files:
            print(unmatched)

    # 随机打乱匹配的文件
    random.shuffle(matched_files)

    # import pdb;pdb.set_trace()
    # 计算分割点
    split_index = int(len(matched_files) * split_ratio)

    # 分割为训练集和测试集
    train_files = matched_files[:split_index]
    test_files = matched_files[split_index:]

    # 复制文件到训练集和测试集文件夹
    for xml_file, image_file in tqdm(train_files, desc="复制训练集文件"):
        shutil.copy(os.path.join(annotations_dir, xml_file), os.path.join(train_dir, 'Annotations', xml_file))
        shutil.copy(os.path.join(images_dir, image_file), os.path.join(train_dir, 'Images', image_file))

    for xml_file, image_file in tqdm(test_files, desc="复制测试集文件"):
        shutil.copy(os.path.join(annotations_dir, xml_file), os.path.join(test_dir, 'Annotations', xml_file))
        shutil.copy(os.path.join(images_dir, image_file), os.path.join(test_dir, 'Images', image_file))

    print("数据集分割完成！")


# 示例用法
annotations_dir = "/home/lgd/e_commerce_lmm/data/OCR_Det_Eval_20200731_e2e/Annotations/"
images_dir = "/home/lgd/e_commerce_lmm/data/OCR_Det_Eval_20200731_e2e/Images/"
train_dir = '/home/lgd/e_commerce_lmm/data/OCR_Det/train'
test_dir = '/home/lgd/e_commerce_lmm/data/OCR_Det/test'

split_dataset(annotations_dir, images_dir, train_dir, test_dir)

# train 4788
# test 533