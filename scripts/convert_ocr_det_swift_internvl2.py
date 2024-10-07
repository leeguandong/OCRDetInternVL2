import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import json
from PIL import Image, ExifTags
import xml.etree.ElementTree as ET


def create_directory(path):
    """Create a new directory at the given path."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory created at {path}"
    except Exception as e:
        return f"An error occurred: {e}"


def list_files(directory):
    """List all files in the given directory."""
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


def list_files_with_absolute_paths(directory):
    """List all files in the given directory with their absolute paths."""
    return [os.path.abspath(os.path.join(directory, file)) for file in os.listdir(directory) if
            os.path.isfile(os.path.join(directory, file))]


def extract_xml_info_old(xml_file_path):
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # 解析XML内容
    root = ET.fromstring(xml_content)

    # 初始化一个列表来保存提取的信息
    extracted_info = []

    # 遍历所有<object>标签
    # import pdb;pdb.set_trace()
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')

        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 将提取的信息保存到列表中
        extracted_info.append({'name': name, 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

    name = str(extracted_info[0]['name'])
    xmin = str(extracted_info[0]['xmin'])
    ymin = str(extracted_info[0]['ymin'])
    xmax = str(extracted_info[0]['xmax'])
    ymax = str(extracted_info[0]['ymax'])
    # 仅仅用于单标注图像
    result = f'<ref>{name}</ref><box>[[{xmin},{ymin},{xmax},{ymax}]]</box>'

    return result

def extract_xml_info(xml_file_path):
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # 解析XML内容
    root = ET.fromstring(xml_content)

    # 初始化一个列表来保存提取的信息
    extracted_info = []

    # 遍历所有<object>标签
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')

        # 提取新的边界框坐标
        x0 = int(bndbox.find('x0').text)
        y0 = int(bndbox.find('y0').text)
        x1 = int(bndbox.find('x1').text)
        y1 = int(bndbox.find('y1').text)
        x2 = int(bndbox.find('x2').text)
        y2 = int(bndbox.find('y2').text)
        x3 = int(bndbox.find('x3').text)
        y3 = int(bndbox.find('y3').text)

        # 将提取的信息保存到列表中
        # -------------------------------------------------------------------------
        extracted_info.append({
            'name': name,
            # 'coordinates': [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
            'coordinates': [(x0, y0), (x2, y2)]
        })

    # 仅仅用于单标注图像
    if extracted_info:
        name = str(extracted_info[0]['name'])
        coords = extracted_info[0]['coordinates']
        result = f'<ref>{name}</ref><box>[[{coords[0][0]},{coords[0][1]},{coords[1][0]},{coords[1][1]}]]</box>'
    else:
        result = '<ref></ref><box>[]</box>'  # 如果没有提取到信息

    return result


def get_elements_with_string(lst, target_string):
    return [element for element in lst if target_string in element]


train_pic_path = "/home/lgd/e_commerce_lmm/data/OCR_Det/train/Images/"
train_xml_path = "/home/lgd/e_commerce_lmm/data/OCR_Det/train/Annotations/"
test_pic_path = "/home/lgd/e_commerce_lmm/data/OCR_Det/test/Images/"
test_xml_path = "/home/lgd/e_commerce_lmm/data/OCR_Det/test/Annotations/"

train_pic_absolute_paths = list_files_with_absolute_paths(train_pic_path)
train_xml_absolute_paths = list_files_with_absolute_paths(train_xml_path)
test_pic_absolute_paths = list_files_with_absolute_paths(test_pic_path)
test_xml_absolute_paths = list_files_with_absolute_paths(test_xml_path)

train_pic_paths = list_files(train_pic_path)
train_xml_paths = list_files(train_xml_path)
test_pic_paths = list_files(test_pic_path)
test_xml_paths = list_files(test_xml_path)

dataset = []

for train_pic_absolute_path in train_pic_absolute_paths:  # 图像路径
    mid_dict = {}
    file_head = train_pic_absolute_path.split('/')[-1].split('.')[0]
    # print(file_head,train_pic_absolute_path)
    xml_path = get_elements_with_string(train_xml_absolute_paths, file_head)[0]
    # print(xml_path)
    xml_info = extract_xml_info(xml_path)  # response
    mid_dict = {
        'system': '''职位：你是一个面向证书图像的目标检测大师，具备精准识别、定位图像中相应位置的能力。
        职能：从各类卡证和票据等图像中检测到相应位置区域并给出边界框。
        **注意**：仅以给定格式返回检测结果，不要给出其它任何解释。
        **注意**：若图片中没有典型场景，返回<ref> class_name </ref><box>[[0, 0, 0, 0]]</box>即可。
        ''',
        'query': '请目标检测图像中的信息并给出边界框',
        'response': xml_info,
        'images': train_pic_absolute_path
    }

    dataset.append(mid_dict)

# 指定输出文件的名称
output_file = '/home/lgd/e_commerce_lmm/data/ocr_det_train_dataset.jsonl'

# 打开文件并写入JSONL格式的数据
with open(output_file, 'w', encoding='utf-8') as f:
    for item in dataset:
        # 将字典转换为JSON字符串并写入文件，每个字典占一行
        json_string = json.dumps(item, ensure_ascii=False)
        f.write(json_string + '\n')

dataset = []

for test_pic_absolute_path in test_pic_absolute_paths:  # 图像路径
    mid_dict = {}
    file_head = test_pic_absolute_path.split('/')[-1].split('.')[0]
    xml_path = get_elements_with_string(test_xml_absolute_paths, file_head)[0]
    xml_info = extract_xml_info(xml_path)  # response
    mid_dict = {
        'system': '''职位：你是一个面向证书图像的目标检测大师，具备精准识别、定位图像中相应位置的能力。
        职能：从各类卡证和票据等图像中检测到相应位置区域并给出边界框。
        **注意**：仅以给定格式返回检测结果，不要给出其它任何解释。
        **注意**：若图片中没有典型场景，返回<ref> class_name </ref><box>[[0, 0, 0, 0]]</box>即可。
        ''',
        'query': '请目标检测图像中的信息并给出边界框',
        'response': xml_info,
        'images': test_pic_absolute_path
    }

    dataset.append(mid_dict)

# 指定输出文件的名称
output_file = '/home/lgd/e_commerce_lmm/data/ocr_det_test_dataset.jsonl'

# 打开文件并写入JSONL格式的数据
with open(output_file, 'w', encoding='utf-8') as f:
    for item in dataset:
        # 将字典转换为JSON字符串并写入文件，每个字典占一行
        json_string = json.dumps(item, ensure_ascii=False)
        f.write(json_string + '\n')
