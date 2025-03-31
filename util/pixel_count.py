"""
统计像素，然后计算白像素占比
"""
import cv2
import numpy as np


def calculate_white_ratio_opencv(image_path, threshold=200):
    # 读取图像并转换为灰度图[1]()[7]()
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("图像读取失败，请检查路径")

    # 二值化处理：大于阈值的设为255（白色），其余为0[7]()[5]()
    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # 计算白色像素数量（向量化操作，效率最高）[6]()[7]()
    white_pixels = np.sum(binary_img == 255)
    total_pixels = binary_img.shape[0] * binary_img.shape[1]
    white_ratio = round((white_pixels / total_pixels) * 100, 2)

    return white_ratio
def detect_defect_ratio(image_path, lower_threshold=30, upper_threshold=100):
    img = cv2.imread(image_path,  cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img,  lower_threshold, upper_threshold, cv2.THRESH_BINARY_INV)
    defect_pixels = cv2.countNonZero(thresh)
    total_pixels = img.size
    ratio = round(defect_pixels / total_pixels * 100, 2)
    return f"缺陷占比: {ratio}%"

# 示例调用
ratio = calculate_white_ratio_opencv(r"C:\1workspace\ai_35\crack_detect\img\output_dir\mask2.png", threshold=200)
print(f"白色像素占比: {ratio}%")

ratio = detect_defect_ratio(r'C:\1workspace\ai_35\crack_detect\img\output_dir\mask2.png')
print(ratio)