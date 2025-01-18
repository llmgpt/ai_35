"""
道路裂缝检测系统
1.加载图片并显示
2.检测按钮，点击检测，得到结果图片显示
3.计算按钮，点击计算，得到一个随机的值

参考图片编写(X)

需要一个完整的项目,生成只是大概，还不如直接借用之前的零售商品系统(X)

一口吃不成胖子，逐步修改。
参照ai_35\day90\work_02_main.py
"""
# 前端页面
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QRadioButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# 后端调用
from ultralytics import YOLO
from method import detect_img



class RoadDamageDetectionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("路面病害检测系统")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        main_layout = QVBoxLayout()

        # 标题标签
        title_label = QLabel("路 面 病 害 检 测", self)
        title_label.setStyleSheet("font-size: 30px; font-weight: bold; text-align: center; color: #2F4F4F;")
        main_layout.addWidget(title_label)

        # 模式选择
        mode_layout = QHBoxLayout()
        self.single_mode = QRadioButton("单张检测")
        self.single_mode.setStyleSheet("color: #4B0082;")
        self.batch_mode = QRadioButton("批量检测")
        self.batch_mode.setStyleSheet("color: #4B0082;")
        mode_layout.addWidget(self.single_mode)
        mode_layout.addWidget(self.batch_mode)
        main_layout.addLayout(mode_layout)

        # 文件路径输入框和按钮
        file_layout = QHBoxLayout()
        self.load_file_button = QPushButton("加载权限重文件")
        self.load_file_button.setStyleSheet("background-color: #FFD700; font-weight: bold;")
        self.save_path_input = QLineEdit()
        self.save_path_input.setPlaceholderText("保存路径")
        self.save_path_input.setStyleSheet("background-color: #F0E68C;")
        self.load_file_button.clicked.connect(self.load_file)
        self.save_path_input.setReadOnly(True)  # 让文本框只读
        file_layout.addWidget(self.load_file_button)
        file_layout.addWidget(self.save_path_input)
        main_layout.addLayout(file_layout)

        # 图片路径和文件夹路径输入框
        img_layout = QHBoxLayout()
        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("图片路径")
        self.image_path_input.setStyleSheet("background-color: #F0E68C;")
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("文件夹路径")
        self.file_path_input.setStyleSheet("background-color: #F0E68C;")

        # 图片路径选择按钮
        self.image_path_button = QPushButton("选择图片路径")
        self.image_path_button.setStyleSheet("background-color: #ADD8E6;")
        self.image_path_button.clicked.connect(self.select_image_path)

        # 文件夹路径选择按钮
        self.folder_path_button = QPushButton("选择文件夹路径")
        self.folder_path_button.setStyleSheet("background-color: #ADD8E6;")
        self.folder_path_button.clicked.connect(self.select_folder_path)

        img_layout.addWidget(self.image_path_input)
        img_layout.addWidget(self.image_path_button)
        img_layout.addWidget(self.file_path_input)
        img_layout.addWidget(self.folder_path_button)
        main_layout.addLayout(img_layout)

        # 显示图片的区域 (加载的图片)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        main_layout.addWidget(self.image_label)

        # 显示图片的区域 (检测时显示的图片)
        self.detection_label = QLabel(self)
        self.detection_label.setAlignment(Qt.AlignCenter)
        self.detection_label.setStyleSheet("border: 1px solid black;")
        main_layout.addWidget(self.detection_label)

        # 开始检测按钮
        start_button = QPushButton("开始检测")
        start_button.setStyleSheet("background-color: #32CD32; color: white; font-weight: bold;")
        start_button.clicked.connect(self.show_detection_image)
        main_layout.addWidget(start_button)

        # 人工修复按钮
        repair_button = QPushButton("人工修复")
        repair_button.setStyleSheet("background-color: #FF6347; color: white; font-weight: bold;")
        main_layout.addWidget(repair_button)

        # 上一张图片和下一张图片按钮
        navigation_layout = QHBoxLayout()
        prev_button = QPushButton("上一张图片")
        prev_button.setStyleSheet("background-color: #00BFFF; color: white;")
        next_button = QPushButton("下一张图片")
        next_button.setStyleSheet("background-color: #00BFFF; color: white;")
        navigation_layout.addWidget(prev_button)
        navigation_layout.addWidget(next_button)
        main_layout.addLayout(navigation_layout)

        self.setLayout(main_layout)

        # 存储选择的图片路径
        self.selected_image_path = ""
        self.detection_image_path = ""

        # 加载模型
        detect_weight_path = '' # 模型路径
        self.detect_model = YOLO(detect_weight_path)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.save_path_input.setText(file_path)

    def select_image_path(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg)")
        if image_path:
            self.image_path_input.setText(image_path)
            self.selected_image_path = image_path
            self.show_image()

    def select_folder_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.file_path_input.setText(folder_path)

    def show_image(self):
        if self.selected_image_path:
            pixmap = QPixmap(self.selected_image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=True))

    def show_detection_image(self):
        # 这里你可以替换为你想要显示的检测图片路径
        self.detection_image_path = r"20160222_164000_1_721_2.png"
        if self.detection_image_path:
            pixmap = QPixmap(self.detection_image_path)
            self.detection_label.setPixmap(pixmap.scaled(self.detection_label.size(), aspectRatioMode=True))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoadDamageDetectionApp()
    window.show()
    sys.exit(app.exec_())
