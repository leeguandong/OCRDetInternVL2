import os
import json
import pyarrow.parquet as pq
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from tqdm import tqdm
from pathlib import Path

# 设置中文字体，替换为你系统中的中文字体路径
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def read_parquet():
    # 读取.parquet文件
    table = pq.read_table(r'E:\comprehensive_library\e_commerce_lmm\data\OCRBench\data\test-00000-of-00001.parquet')

    # 将table转换为DataFrame
    df = table.to_pandas()

    # 打印DataFrame
    print(df)


def process_chineseocrbench_jsonl(input_file, output_file):
    new_format_json = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line.strip())
                if 'dataset_name' in item and 'file_name' in item:
                    image_path = f"{item['dataset_name']}/{item['file_name']}"
                    new_item = {
                        "dataset_name": item["dataset_name"],
                        "id": item.get("id", 0),  # 如果原始数据中没有'id'字段，设置默认值
                        "image_path": image_path,
                        "question": item.get("question", "what is written in the image?"),
                        "answers": item.get("answers", ""),  # 如果原始数据中没有'answers'字段，设置默认值
                        "type": item.get("type", "Text Recognition")  # 如果原始数据中没有'type'字段，设置默认值
                    }
                    new_format_json.append(new_item)
            except json.JSONDecodeError as e:
                print(f"Ignoring line due to JSONDecodeError: {e}")
                continue

    # 将处理后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_format_json, f, ensure_ascii=False, indent=4)

    print(f"处理后的数据已写入到 {output_file}")


def draw_boxes_from_xml(xml_file, image_file):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get image size from XML
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    # Load image
    image = Image.open(image_file)

    # Create figure and axes
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Iterate through each object in XML
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        x0 = int(bndbox.find('x0').text)
        y0 = int(bndbox.find('y0').text)
        x1 = int(bndbox.find('x1').text)
        y1 = int(bndbox.find('y1').text)
        x2 = int(bndbox.find('x2').text)
        y2 = int(bndbox.find('y2').text)
        x3 = int(bndbox.find('x3').text)
        y3 = int(bndbox.find('y3').text)

        # Draw rectangle
        polygon = patches.Polygon([(x0, y0), (x1, y1), (x2, y2), (x3, y3)], closed=True, fill=None, edgecolor='red')
        ax.add_patch(polygon)

        # Add label
        ax.text(x0, y0, name, bbox=dict(facecolor='red', alpha=0.5))

    # Set plot title
    plt.title('Image with Bounding Boxes')

    # Display the plot
    plt.axis('off')  # turn off axis labels
    plt.show()


def generate_description_from_xml(xml_file):
    # 解析XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 存储每个object的信息
    objects = []

    # 提取object信息
    for obj in root.findall('object'):
        try:
            name = obj.find('name').text
            if '#' in name:
                # 如果名称中包含'#'，则过滤掉含有'#'的部分
                name = name.split('#')[0].strip()
            bndbox = obj.find('bndbox')
            x0 = int(bndbox.find('x0').text)
            y0 = int(bndbox.find('y0').text)
            x1 = int(bndbox.find('x1').text)
            y1 = int(bndbox.find('y1').text)
            # 计算中心点的y坐标，用于排序
            center_y = (y0 + y1) / 2
            objects.append((name, x0, y0, x1, y1, center_y))
        except Exception as e:
            print(f"Error processing object: {e}")
            continue  # 出现异常时跳过当前循环继续处理下一个object

    # 按照y坐标排序，然后按照x坐标排序
    objects_sorted = sorted(objects, key=lambda x: (x[5], x[1]))

    # 生成描述
    description = []
    for obj in objects_sorted:
        name = obj[0]
        description.append(name)

    final_description = " ".join(description)
    return final_description


def post_process_description(description):
    # 后处理：如果描述中出现了"招商银行"，则将其替换为"银行"
    for i in range(len(description)):
        if "招商银行" in description[i]:
            description[i] = "银行"

    final_description = " ".join(description)
    return final_description


def process_images_and_xmls(root_folder, exclude_folders, xml_folder):
    # 遍历根文件夹下的所有文件夹
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)

        # 排除指定的文件夹
        if os.path.isdir(folder_path) and folder not in exclude_folders:
            result = []
            idx = 0
            # 获取第二级文件夹下的图片文件
            image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]

            for image_file in tqdm(image_files):
                # 构建图片路径
                image_path = os.path.join(folder_path, image_file).replace('\\', '/')

                # 构建对应的XML文件路径（假设图片文件名和XML文件名对应，只是后缀不同）
                xml_file = os.path.join(xml_folder, os.path.splitext(image_file)[0] + '.xml').replace('\\', '/')

                # 如果对应的XML文件存在，则处理
                if os.path.exists(xml_file):
                    # 生成描述
                    description = generate_description_from_xml(xml_file)
                    # 后处理描述
                    # description = post_process_description(description)

                    path = Path(image_path)
                    path = str(path.relative_to(path.parents[1]))

                    if folder == "bankCard":
                        question = "这张银行卡上的内容是什么？"
                    elif folder == "ICDAR13" or folder == "ICDAR15":
                        question = "what is written in the image?"
                    else:
                        question = "这张图上的文字是什么？"

                    # 构建数据项
                    data_item = {
                        "dataset_name": folder,
                        "id": idx,
                        "image_path": path,
                        "question": question,
                        "answers": description,
                        "type": "OCR"
                    }

                    # 添加到结果列表
                    result.append(data_item)
                    idx += 1

            # 保存为单独的JSON文件
            output_file = f"{folder}_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            print(f"Processed {len(result)} images from {folder}. Saved output to {output_file}.")


def merge_json_files(input_folder, output_file):
    """
    Merge all JSON files in the specified folder into one JSON file.
    Replace '\\' in 'image_path' with '/' during merging.
    Recalculate 'id' for each object starting from 1.

    Args:
    - input_folder (str): Path to the folder containing JSON files.
    - output_file (str): Path to the output JSON file where merged data will be saved.
    """

    # Initialize an empty list to store all JSON objects
    all_data = []

    # Traverse each JSON file in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)

    # Modify 'image_path' by replacing '\\' with '/'
    for item in all_data:
        item['image_path'] = item['image_path'].replace('\\', '/')

    # Recalculate 'id' for each object starting from 1
    for index, item in enumerate(all_data):
        item['id'] = index + 1

    # Write merged data to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f'Merged JSON data saved to {output_file}')


def merge_specific_json_files(input_files, output_file):
    """
    Merge specific JSON files into one JSON file.
    Replace '\\' in 'image_path' with '/' during merging.
    Recalculate 'id' for each object starting from 1.

    Args:
    - input_files (list of str): List of paths to JSON files to merge.
    - output_file (str): Path to the output JSON file where merged data will be saved.
    """

    # Initialize an empty list to store all JSON objects
    all_data = []

    # Traverse each JSON file in the input_files list
    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    # Modify 'image_path' by replacing '\\' with '/'
    for item in all_data:
        item['image_path'] = item['image_path'].replace('\\', '/')

    # Recalculate 'id' for each object starting from 1
    for index, item in enumerate(all_data):
        item['id'] = index + 1

    # Write merged data to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f'Merged JSON data saved to {output_file}')


if __name__ == "__main__":
    # 调用函数示例
    # input_file = r'E:\comprehensive_library\e_commerce_lmm\data\ChineseOCRBench\data\metadata.jsonl'
    # output_file = 'processed_data.json'
    # process_chineseocrbench_jsonl(input_file, output_file)

    # Example usage
    xml_file = r'D:\datasets\OCR_Det_Eval_20200731_e2e\Annotations\bankCard_100.xml'
    image_file = r'E:\comprehensive_library\e_commerce_lmm\data\EcommerceOCRBench\data\EcommOCRBench_Images\bankCard\bankCard_100.jpg'
    # draw_boxes_from_xml(xml_file, image_file)

    # generated_description = generate_description_from_xml(xml_file)
    # print("Generated Description:", generated_description)

    root_folder = "E:/comprehensive_library/e_commerce_lmm/data/EcommerceOCRBench/data/EcommOCRBench_Images"
    xml_folder = "D:/datasets/OCR_Det_Eval_20200731_e2e/Annotations"
    exclude_folders = ['ReCTS', 'ESTVQA_cn', 'annotations']  # 替换成你希望排除的第二级文件夹列表

    # process_images_and_xmls(root_folder, exclude_folders, xml_folder)

    input_folder = r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations'
    output_file = r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\Total_EcommerceOCRBench.json'
    # merge_json_files(input_folder, output_file)

    input_files = [
        r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations\ICDAR13_output.json',
        r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations\ICDAR15_output.json',
        r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations\MTWI2018_output.json',
        r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations\RCTW17_output.json',
        r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\annotations\EcommOCRBench.json'
    ]
    output_file = r'E:\comprehensive_library\e_commerce_lmm\evaluation\EcommerceOCRBench\bench\Specific_EcommerceOCRBench.json'
    merge_specific_json_files(input_files, output_file)
