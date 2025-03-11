"单个labelme生成的json转黑白mask"
import json
import cv2
import numpy as np

def create_mask_from_json(json_file, output_mask_path):
    # 读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 获取图像的宽度和高度
    img_height = data['imageHeight']
    img_width = data['imageWidth']

    # 创建一个全黑的掩码图像
    mask = np.zeros((img_height, img_width), dtype=np.uint8)

    # 遍历每个标注对象
    for shape in data['shapes']:
        points = np.array(shape['points'], dtype=np.int32)
        # 填充多边形区域为白色
        cv2.fillPoly(mask, [points], 255)

    # 保存掩码图像
    cv2.imwrite(output_mask_path, mask)

def create_mask_with_random_drops(json_file, output_mask_path, drop_rate=0.1):
    # 读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 获取图像的宽度和高度
    img_height = data['imageHeight']
    img_width = data['imageWidth']

    # 创建一个全黑的掩码图像
    mask = np.zeros((img_height, img_width), dtype=np.uint8)

    # 遍历每个标注对象
    for shape in data['shapes']:
        points = np.array(shape['points'], dtype=np.int32)
        # 填充多边形区域为白色
        cv2.fillPoly(mask, [points], 255)

    # 随机丢弃一些像素
    if drop_rate > 0:
        random_mask = np.random.rand(img_height, img_width) < drop_rate
        mask[random_mask] = 0

    # 保存掩码图像
    cv2.imwrite(output_mask_path, mask)

# 示例用法
json_file = r'C:\1workspace\ai_35\crack_detect\img\output_dir\img2.json'
output_mask_path = r'C:\1workspace\ai_35\crack_detect\img\output_dir\mask2.png'
create_mask_with_random_drops(json_file, output_mask_path)