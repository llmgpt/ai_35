# 千问太强大了
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton,
    QGroupBox, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class DiseaseDetectionSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("病害分割系统")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {background: #f5f5f5;}
            QLabel {font-family: 'Microsoft YaHei';}
        """)

        # 主容器
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setCentralWidget(container)

        # 左侧区域
        left_widget = QWidget()
        left_widget.setStyleSheet("background: white; border-radius: 10px;")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)

        # 标题栏
        title_bar = QLabel("路面病害智能分割系统")
        title_bar.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title_bar.setAlignment(Qt.AlignCenter)
        title_bar.setStyleSheet("background: #2196F3; color: white; border-radius: 8px; padding: 12px;")
        left_layout.addWidget(title_bar)

        # 输入图片区域
        self.input_image = QLabel("等待选择图片...")
        self.input_image.setAlignment(Qt.AlignCenter)
        self.input_image.setStyleSheet("border: 2px dashed #e0e0e0; background: #fafafa; color: #757575;")
        self.input_image.setFixedSize(540, 340)
        self.input_image.setScaledContents(True)
        left_layout.addWidget(self.input_image)

        # 输出图片区域
        self.output_image = QLabel("分割结果将显示在此处")
        self.output_image.setAlignment(Qt.AlignCenter)
        self.output_image.setStyleSheet("border: 2px dashed #64b5f6; background: #fafafa; color: #757575;")
        self.output_image.setFixedSize(540, 340)
        self.output_image.setScaledContents(True)
        left_layout.addWidget(self.output_image)

        # 右侧区域
        right_widget = QWidget()
        right_widget.setStyleSheet("background: white; border-radius: 10px;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # 分割模式
        mode_group = QGroupBox("分割模式")
        mode_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2196F3;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        mode_layout = QHBoxLayout()

        self.mode = "single"
        self.single_btn = QPushButton("单张分割")
        self.batch_btn = QPushButton("批量分割")

        self.single_btn.setStyleSheet(self.get_mode_style("#4CAF50"))
        self.batch_btn.setStyleSheet(self.get_mode_style("#FF9800", checked=False))

        self.single_btn.clicked.connect(lambda: self.set_mode("single"))
        self.batch_btn.clicked.connect(lambda: self.set_mode("batch"))

        mode_layout.addWidget(self.single_btn)
        mode_layout.addWidget(self.batch_btn)
        mode_group.setLayout(mode_layout)
        right_layout.addWidget(mode_group)

        # 配置区域
        config_group = QGroupBox("参数配置")
        config_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2196F3;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.config_layout = QVBoxLayout()
        self.config_layout.setSpacing(10)
        config_group.setLayout(self.config_layout)

        # 权重文件
        self.weight_path = QLineEdit()
        self.weight_path.setPlaceholderText("请选择权重文件...")
        self.add_config_row(config_group, "加载权重文件", self.weight_path, "选择文件", "*.pdparams *.pth")

        # 保存路径
        self.save_path = QLineEdit()
        self.save_path.setPlaceholderText("请选择保存路径...")
        self.add_config_row(config_group, "保存路径", self.save_path, "选择路径", is_folder=True)

        # 图片路径（合并加载功能）
        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("请选择图片路径...")
        self.add_config_row(config_group, "图片路径", self.image_path, "选择图片", "*.jpg *.png",
                            on_select=self.update_input_image)

        # 文件夹路径
        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("请选择文件夹路径...")
        self.add_config_row(config_group, "文件夹路径", self.folder_path, "选择目录", is_folder=True)

        right_layout.addWidget(config_group)
        # 在right_layout.addWidget(config_group) 之后添加以下代码

        # ========== PCI计算模块 ==========
        pci_group = QGroupBox("路面状况评估")
        pci_group.setStyleSheet(""" 
            QGroupBox {
                font-weight: bold;
                color: #2196F3;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        pci_layout = QVBoxLayout()

        # PCI值显示标签
        self.pci_value_label = QLabel("PCI: 未计算")
        self.pci_value_label.setStyleSheet(""" 
            QLabel {
                font-size: 24px;
                color: #4CAF50;
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
                text-align: center;
            }
        """)
        pci_layout.addWidget(self.pci_value_label)

        # 计算按钮
        self.calc_pci_btn = QPushButton("计算PCI")
        self.calc_pci_btn.setStyleSheet(""" 
            QPushButton {
                background: #9C27B0;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7B1FA2;
            }
            QPushButton:disabled {
                background: #BDBDBD;
            }
        """)
        self.calc_pci_btn.clicked.connect(self.calculate_pci)
        pci_layout.addWidget(self.calc_pci_btn)

        pci_group.setLayout(pci_layout)
        right_layout.addWidget(pci_group)  # 插入到参数配置组下方


        # 控制按钮
        detect_btn = QPushButton("开始分割")
        detect_btn.setStyleSheet(self.get_control_style("#2196F3"))
        detect_btn.clicked.connect(self.start_detection)
        right_layout.addWidget(detect_btn)

        modify_btn = QPushButton("人工修正")
        modify_btn.setStyleSheet(self.get_control_style("#ff5722"))
        modify_btn.clicked.connect(self.manual_modify)
        right_layout.addWidget(modify_btn)

        # 导航按钮
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("‹ 上一张")
        next_btn = QPushButton("下一张 ›")
        prev_btn.setStyleSheet(self.get_nav_style())
        next_btn.setStyleSheet(self.get_nav_style())
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(next_btn)
        right_layout.addLayout(nav_layout)

        right_layout.addStretch()

        # 将左右区域加入主布局
        main_layout.addWidget(left_widget, 3)
        main_layout.addWidget(right_widget, 2)

    def get_mode_style(self, color, checked=True):
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self.adjust_color(color, 1.2)};
            }}
            QPushButton:checked {{
                background: {self.adjust_color(color, 0.8)};
                border: 2px solid {color};
            }}
        """ if checked else f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self.adjust_color(color, 1.2)};
            }}
        """

    def get_control_style(self, color):
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 14px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self.adjust_color(color, 0.9)};
            }}
        """

    def get_nav_style(self):
        return """
            QPushButton {
                background: #607d8b;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #546e7a;
            }
        """

    def adjust_color(self, color, factor):
        c = QColor(color)
        return QColor(
            min(int(c.red() * factor), 255),
            min(int(c.green() * factor), 255),
            min(int(c.blue() * factor), 255)
        ).name()

    def add_config_row(self, parent_group, label, line_edit, btn_text,
                       ext_filter=None, is_folder=False, on_select=None):
        hbox = QHBoxLayout()
        line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                background: #fafafa;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        hbox.addWidget(line_edit, 4)

        btn = QPushButton(btn_text)
        btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #1e88e5;
            }
        """)

        if on_select:
            btn.clicked.connect(lambda: (self.select_path(line_edit, ext_filter, is_folder), on_select()))
        else:
            btn.clicked.connect(lambda: self.select_path(line_edit, ext_filter, is_folder))

        hbox.addWidget(btn, 1)

        line_edit.setMaximumHeight(30)
        hbox.setSpacing(8)
        parent_group.layout().addLayout(hbox)

    def select_path(self, line_edit, ext_filter=None, is_folder=False):
        if is_folder:
            path = QFileDialog.getExistingDirectory(self, "选择目录")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", ext_filter)

        if path:
            line_edit.setText(path)

    def update_input_image(self):
        path = self.image_path.text()
        if path:
            pixmap = QPixmap(path)
            self.input_image.setPixmap(pixmap.scaled(
                self.input_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def start_detection(self):
        # 模拟分割过程
        if not self.image_path.text():
            QMessageBox.warning(self, "错误", "请先选择图片")
            return

        # 模拟分割结果
        result_path = r'C:\1workspace\ai_35\crack_detect\img\output_dir\mask.png'
        self.output_pixmap = QPixmap(result_path)
        self.output_image.setPixmap(self.output_pixmap.scaled(
            self.output_image.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        QMessageBox.information(self, "完成", "分割已完成！")

    def manual_modify(self):
        QMessageBox.information(self, "提示", "人工修正功能尚未实现")

    def calculate_pci(self):
        pci = 92.288
        self.pci_value_label.setText(f"PCI:  {pci:.2f}")
        self.pci_value_label.setStyleSheet("color:  #4CAF50; font-size: 24px;")
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiseaseDetectionSystem()
    window.show()
    sys.exit(app.exec_())