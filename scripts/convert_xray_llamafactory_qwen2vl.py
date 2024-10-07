import json

# 读取JSON文件
input_file_path = r'E:\comprehensive_library\e_commerce_lmm\data\open-zh-swift-llava-prompt.json'  # 请将此路径替换为您的JSON文件路径
with open(input_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换后的数据
converted_data = []

for item in data:
    conversation = [
        {
            "from": "human",
            "value": "<image>" + item["query"]  # 添加 <image> 标签
        },
        {
            "from": "gpt",
            "value": item["response"]
        }
    ]

    images = [img.replace('/home/image_team/image_team_docker_home/lgd/e_commerce_lmm/data/XrayGLM/',
                          '/home/lgd/e_commerce_lmm/data/XrayGLM/') for img in item["images"]]

    converted_data.append({
        "conversations": conversation,
        "images": images
    })

# 输出转换后的数据到新的JSON文件
output_file_path = "../data/openai-zh-llamafactory-qwen2vl-prompt.json"  # 请将此路径替换为您希望保存的输出文件路径
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=2)

print("转换完成，结果已保存到", output_file_path)