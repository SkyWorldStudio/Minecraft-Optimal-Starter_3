# coding=utf-8
import os.path

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect
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
            self.Animation_ToMainWindow()

    def FirstStartInitialize(self):
        """在第一次启动时 初始化(缓存)"""
        from Code.Code import InitializeFirst
        InitializeFirst()
        self.stackedWidget_main.setCurrentIndex(1)

    def Animation_ToMainWindow(self):
        """动画函数-加载页面->主页面"""
        # 设置透明度
        self.Opacity = QGraphicsOpacityEffect()  # 透明度对象
        self.Opacity.setOpacity(1)  # 初始化设置透明度为，即不透明
        # self.label.setGraphicsEffect(self.Opacity)  # 把标签的透明度设置为为self.opacity

        self.Animation_ToMainWindow_Int_Original = 1  # 原来多少
        self.Animation_ToMainWindow_Int = 0.05  # 每次淡化多少

        def Animation():
            """淡出"""
            self.Animation_ToMainWindow_Int_Original -= self.Animation_ToMainWindow_Int
            if self.Animation_ToMainWindow_Int_Original < 0:
                self.Animation_ToMainWindow_Run.stop()
                self.stackedWidget_main.setCurrentIndex(0)

                # 开始淡入
                self.Animation_ToMainWindow_Int_Original = 0  # 原来多少
                self.Animation_ToMainWindow_Int = 0.05  # 每次淡入多少
                self.Opacity.setOpacity(0)  # 为了防止出现负数 所以重新设置

                # 触发切换动画(淡入)
                self.Animation_ToMainWindow_Run_In = QTimer()
                self.Animation_ToMainWindow_Run_In.start(2)
                self.Animation_ToMainWindow_Run_In.timeout.connect(AnimationIn)

            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        def AnimationIn():
            """淡入"""
            self.Animation_ToMainWindow_Int_Original += self.Animation_ToMainWindow_Int
            if self.Animation_ToMainWindow_Int_Original > 1:
                self.Animation_ToMainWindow_Run_In.stop()
            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        # 触发切换动画(淡出)
        self.Animation_ToMainWindow_Run = QTimer()
        self.Animation_ToMainWindow_Run.start(2)
        self.Animation_ToMainWindow_Run.timeout.connect(Animation)

def Run():
    print("程序已开始运行！")
    app = QtWidgets.QApplication(sys.argv)
    print("创建窗口对象成功！")
    ui = RunUi()
    print("创建PyQt窗口对象成功！")
    sys.exit(app.exec())
