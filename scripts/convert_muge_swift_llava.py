import json

# 打开并读取 JSON 文件
with open(r"E:\comprehensive_library\e_commerce_lmm\data\IC_valid.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)

new_format_data = []

for item in data:
    conversations = item.get('conversations', [])
    # 提取图片路径
    img_start = conversations[0]['value'].find('<img>') + 5
    img_end = conversations[0]['value'].find('</img>')
    image_path = conversations[0]['value'][img_start:img_end]

    # 提取用户查询和助手回复
    query = conversations[0]['value'].replace(f'<img>{image_path}</img>\n', '').replace("Picture 1:", "")
    response = conversations[1]['value']

    # 更新到新数据格式
    new_format_item = {"query": query, "response": response, "images": [image_path]}
    new_format_data.append(new_format_item)

# 将新格式的数据保存为 JSON 文件
with open('output.json', 'w', encoding="utf-8") as f:
    json.dump(new_format_data, f, ensure_ascii=False, indent=4)
