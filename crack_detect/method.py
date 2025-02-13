"""
后端调用
"""
from PIL import Image
import os
def detect_img(frame, detect_model, image_path):  # 画框，并添加了image_path参数
    results = detect_model(frame)  # 使用YOLO模型检测
    for r in results:
        # Plot results image
        im_bgr = r.plot(conf=False, pil=True, masks=False, labels=False)  # BGR-order numpy array
        im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image

        # 创建result文件夹
        result_dir = os.path.join(os.path.dirname(image_path), 'result')
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # 保存图像到result文件夹
        result_path = os.path.join(result_dir, os.path.basename(image_path))
        im_rgb.save(result_path)

    return result_path
