import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import os  # 添加os模块用于文件操作

# 创建保存增强图像的目录
os.makedirs('augmented_images', exist_ok=True)

# 加载示例图像（替换为实际路径）
img = cv2.imread(r"C:\1workspace\ai_35\crack_detect\img\20160222_164000_1_721.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV默认BGR转RGB


def multi_scale_resize(img, scales=[0.5, 1.0, 1.5]):
    resized_imgs = []
    h, w = img.shape[:2]
    for scale in scales:
        new_size = (int(w * scale), int(h * scale))
        resized = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
        resized_imgs.append(resized)
    return resized_imgs


scales = [0.5, 1.0, 1.5]
resized_images = multi_scale_resize(img, scales)


def random_pad_crop(img, pad_ratio=0.2, crop_size=(256, 256)):
    h, w = img.shape[:2]
    pad_h = int(h * pad_ratio * random.uniform(0, 1))
    pad_w = int(w * pad_ratio * random.uniform(0, 1))

    # 随机颜色填充（可替换为边缘复制或高斯噪声）
    padded = cv2.copyMakeBorder(img, pad_h, pad_h, pad_w, pad_w,
                                cv2.BORDER_CONSTANT, value=(0, 0, 0))

    # 随机裁剪
    y = random.randint(0, padded.shape[0] - crop_size[0])
    x = random.randint(0, padded.shape[1] - crop_size[1])
    cropped = padded[y:y + crop_size[0], x:x + crop_size[1]]
    return cropped


pad_cropped = random_pad_crop(img)


def horizontal_flip(img, p=0.5):
    if random.random() < p:
        return cv2.flip(img, 1)
    else:
        return img


flipped = horizontal_flip(img)


def color_jitter(img, hue=0.1, saturation=0.3, brightness=0.3):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # 随机扰动参数
    h = random.uniform(-hue, hue) * 179  # 色相范围0-179
    s = random.uniform(-saturation, saturation) * 255
    v = random.uniform(-brightness, brightness) * 255

    img_hsv = img_hsv.astype(np.float32)
    img_hsv[..., 0] = np.clip(img_hsv[..., 0] + h, 0, 179)  # 色相
    img_hsv[..., 1] = np.clip(img_hsv[..., 1] + s, 0, 255)  # 饱和度
    img_hsv[..., 2] = np.clip(img_hsv[..., 2] + v, 0, 255)  # 明度

    return cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


jittered = color_jitter(img)

# 保存多尺度缩放图像
for scale, resized in zip(scales, resized_images):
    # 转换回BGR格式并保存
    resized_bgr = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f'augmented_images/scale_{scale}.jpg', resized_bgr)

# 保存随机填充裁剪图像
pad_cropped_bgr = cv2.cvtColor(pad_cropped, cv2.COLOR_RGB2BGR)
cv2.imwrite('augmented_images/pad_cropped.jpg', pad_cropped_bgr)

# 保存水平翻转图像
flipped_bgr = cv2.cvtColor(flipped, cv2.COLOR_RGB2BGR)
cv2.imwrite('augmented_images/flipped.jpg', flipped_bgr)

# 保存颜色扰动图像
jittered_bgr = cv2.cvtColor(jittered, cv2.COLOR_RGB2BGR)
cv2.imwrite('augmented_images/jittered.jpg', jittered_bgr)

plt.figure(figsize=(15, 10))

# 原始图像
plt.subplot(2, 3, 1)
plt.imshow(img)
plt.title("Original")

# 多尺度缩放
for i, (scale, resized) in enumerate(zip(scales, resized_images)):
    plt.subplot(2, 3, i + 2)
    plt.imshow(resized)
    plt.title(f"Scale:  {scale}x")

# 随机填充裁剪
plt.subplot(2, 3, 4)
plt.imshow(pad_cropped)
plt.title("Pad+Crop")

# 水平翻转
plt.subplot(2, 3, 5)
plt.imshow(flipped)
plt.title("Horizontal  Flip")

# 颜色扰动
plt.subplot(2, 3, 6)
plt.imshow(jittered)
plt.title("Color  Jitter")

plt.tight_layout()
plt.show()