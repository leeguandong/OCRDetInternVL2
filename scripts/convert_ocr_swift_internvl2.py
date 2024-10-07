import json


def convert_json_format(file1_path, file2_path, output_file_path):
    """
    将两个json文件转换为目标格式，添加图像路径前缀，并保存到jsonl文件。

    Args:
        file1_path: 第一个json文件的路径。
        file2_path: 第二个json文件的路径。
        output_file_path: 输出文件的路径。

    Returns:
        如果成功，返回 True；如果失败，返回错误消息字符串。
    """

    image_prefix = "/home/lgd/e_commerce_lmm/data/EcommOCRBench_Images/"

    try:
        with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    except FileNotFoundError:
        return "文件未找到，请检查路径。"
    except json.JSONDecodeError:
        return "JSON解码错误，请检查文件格式。"

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for item in data1 + data2:
                converted_item = {
                    "query": item["question"],
                    "response": item["answers"],
                    "images": [image_prefix + item["image_path"]]
                }
                json.dump(converted_item, outfile, ensure_ascii=False)
                outfile.write('\n')  # jsonl格式需要每行一个JSON对象
        return True
    except Exception as e:
        return f"保存文件时出错: {e}"


# 示例用法：
# 示例用法：
file1_path = r"E:\comprehensive_library\e_commerce_lmm\data\EcommerceOCRBench\annotations\EcommOCRBench.json"  # 替换为第一个json文件的实际路径
file2_path = r"E:\comprehensive_library\e_commerce_lmm\data\EcommerceOCRBench\annotations\RCTW17_output.json"  # 替换为第二个json文件的实际路径
output_file_path = "../data/EcommerceOCRBench/ESTVQA_cn_rectw17_ocr_swift.jsonl"  # 指定输出文件名

result = convert_json_format(file1_path, file2_path, output_file_path)

if result is True:
    print(f"数据已成功保存到 {output_file_path}")
else:
    print(result)
