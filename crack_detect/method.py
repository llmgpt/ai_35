"""
后端调用
"""
from PIL import Image
def detect_img(frame, detect_model): # 画框
    results = detect_model(frame)  # 使用YOLO模型检测
    for r in results:
        # Plot results image
        im_bgr = r.plot(conf=False, pil=True, masks=False, labels=False)  # BGR-order numpy array
        im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image
        return im_rgb