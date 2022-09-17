# coding=utf-8
import os.path

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer
import sys
from UI.MainWindow.MainWindow import Ui_MainWindow


class RunUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RunUi, self).__init__()
        self.setupUi(self)
        self.show()
        print("已成功显示窗体")
        self.RunInitialize_ = QTimer()
        self.RunInitialize_.start(10)
        self.RunInitialize_.timeout.connect(self.RunInitialize)
        self.pushButton_hello_start.clicked.connect(self.FirstStartInitialize)

    def RunInitialize(self):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""
        self.RunInitialize_.stop()
        self.JsonFile = os.path.join('')
        from Code.Code import JsonRead, JsonFile, InitializeFirst
        F = JsonFile()
        if os.path.isfile(F) == False:
            """如果没有Json这个目录 就转到欢迎(初始化)页面"""
            self.stackedWidget_main.setCurrentIndex(2)
        else:
            # 如果有 就进行下一步
            a = JsonRead(F)
            print('Json读取完成')
            self.label_loading_text_2.setText('正在设置启动器(2/2)')

    def FirstStartInitialize(self):
        """在第一次启动时 初始化(缓存)"""
        from Code.Code import InitializeFirst
        InitializeFirst()
        self.stackedWidget_main.setCurrentIndex(1)


def Run():
    print("程序已开始运行！")
    app = QtWidgets.QApplication(sys.argv)
    print("创建窗口对象成功！")
    ui = RunUi()
    print("创建PyQt窗口对象成功！")
    sys.exit(app.exec())
