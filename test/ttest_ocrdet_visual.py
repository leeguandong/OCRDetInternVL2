import pandas as pd
from PIL import Image, ImageDraw
import re
import json
from PIL import Image, ExifTags


# 添加这个函数来处理图片方向
def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # 如果没有EXIF信息，就不做任何处理
        pass
    return image


def draw_rectangle(image_path, coordinates, output_path):
    """
    在图像上标出矩形框。

    :param image_path: 图像的路径
    :param coordinates: 包含矩形框坐标的列表，格式为 [x1, y1, x2, y2]
    :param output_path: 输出图像的路径
    """
    # 打开图像
    with Image.open(image_path) as img:
        img = correct_image_orientation(img)
        img = correct_image_orientation(img)
        # 创建一个可以在给定图像上绘图的对象
        draw = ImageDraw.Draw(img)
        # 计算矩形的左上角和右下角坐标
        x1, y1, x2, y2 = coordinates
        # 在图像上绘制矩形
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        # 保存修改后的图像
        img.save(output_path)


def extract_string(s):
    """
    从给定的字符串中提取方括号内的内容。

    :param s: 包含方括号的字符串
    :return: 提取出的字符串
    """
    # 使用正则表达式匹配方括号内的内容
    match = re.search(r'\[(.*?)\]', s)
    if match:
        # 提取匹配的内容
        extracted_str = match.group(0)
        return eval(extracted_str + ']')
    else:
        return None


def read_jsonl(file_path):
    """
    读取JSONL文件并返回一个包含所有条目的列表。

    :param file_path: JSONL文件的路径
    :return: 包含JSON对象的列表
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data


data = pd.read_excel(r'E:\comprehensive_library\e_commerce_lmm\test\llm_response.xlsx')

images = data['images'].tolist()
responses = data['response'].tolist()
n = len(images)

print(images)
for index in range(n):
    try:
        print(images[index])
        img_path = images[index]
        zuobiao = extract_string(responses[index])
        draw_rectangle(img_path, zuobiao[0],
                       'E:/comprehensive_library/e_commerce_lmm/results/internvl2_swift_ocrdet/results' + '/' +
                       img_path.split('/')[-1])
    except:
        pass
