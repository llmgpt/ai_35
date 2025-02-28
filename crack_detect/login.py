"""
登录注册界面
"""
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QLineEdit, QPushButton, QWidget)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QBrush
from PyQt5.QtCore import Qt, QRect


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" 可视化道路病害量化提取系统")  # 设置窗口标题
        self.setFixedSize(1200, 800)  # 固定窗口尺寸

        # 设置背景（需准备road_bg.jpg 图片）
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("img/background.jpg").scaled(self.size()))
        self.background.setGeometry(0, 0, 1200, 800)

        # 绘制标题 
        self.title = QLabel("可视化道路病害量化提取系统", self)
        self.title.setGeometry(200, 50, 800, 80)
        self.title.setStyleSheet(""" 
            QLabel {
                font: bold 32px '微软雅黑';
                color: #000000;
            }
        """)
        self.title.setAlignment(Qt.AlignCenter)

        # 账号输入框
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(400, 250, 400, 50)
        self.username_input.setPlaceholderText(" 请输入账号")
        self.username_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 0 10px;
                font: 18px;
            }
        """)

        # 密码输入框
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(400, 350, 400, 50)
        self.password_input.setPlaceholderText(" 请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(""" 
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 0 10px;
                font: 18px;
            }
        """)

        # 登录按钮 
        self.login_btn = QPushButton("登录", self)
        self.login_btn.setGeometry(400, 450, 180, 50)
        self.login_btn.setStyleSheet(""" 
            QPushButton {
                background: #0078d4;
                color: white;
                border-radius: 10px;
                font: bold 20px;
            }
            QPushButton:hover {
                background: #006cbd;
            }
        """)

        # 注册按钮 
        self.register_btn = QPushButton("注册", self)
        self.register_btn.setGeometry(620, 450, 180, 50)
        self.register_btn.setStyleSheet(""" 
            QPushButton {
                background: #0078d4;
                color: white;
                border-radius: 10px;
                font: bold 20px;
            }
            QPushButton:hover {
                background: #006cbd;
            }
        """)

    def paintEvent(self, event):
        """绘制动态元素：风力发电机和白云"""
        painter = QPainter(self)

        # 绘制风力发电机 
        painter.setBrush(QColor(192, 192, 192))
        # 左侧发电机 
        painter.drawRect(150, 400, 20, 150)  # 塔架
        painter.drawLine(160, 300, 160, 400)  # 支撑杆
        painter.setBrush(QColor(135, 206, 250))  # 叶片颜色
        painter.drawEllipse(135, 270, 50, 50)  # 叶片

        # 右侧发电机 
        painter.drawRect(950, 380, 20, 170)
        painter.drawLine(960, 280, 960, 380)
        painter.drawEllipse(935, 250, 50, 50)

        # 绘制白云 
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(300, 100, 80, 60)
        painter.drawEllipse(350, 110, 100, 70)
        painter.drawEllipse(800, 150, 120, 80)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_()) 