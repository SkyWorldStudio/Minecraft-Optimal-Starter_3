# coding=utf-8
import os.path

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QThread, Qt, QRect, QPropertyAnimation
import sys
from UI.MainWindow.MainWindow import Ui_MainWindow


class RunUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RunUi, self).__init__()

        import UI.MainWindow.img_rc
        import UI.Gif_rc

        self.setupUi(self)
        self.show()
        print("已成功显示窗体")

        self.RunInitialize_ = QTimer()
        self.RunInitialize_.setInterval(20)
        self.RunInitialize_.timeout.connect(self.RunInitialize)
        self.RunInitialize_.start()

        self.pushButton_hello_start.clicked.connect(self.FirstStartInitialize)

        self.label_Sidebar_User.clicked.connect(self.User_Clicked)

    def User_Clicked(self):
        print("用户点击'用户'按钮")

        self.label_Sidebar_User_QTime_B = -1  # 步长
        self.label_Sidebar_User_QTime_Start = 30  # 最小(起始数值)
        self.label_Sidebar_User_QTime_Stop = 0  # 最大(终止数值)
        self.label_Sidebar_User_QTime_N = int(self.label_Sidebar_User_QTime_Start)  # 记录第几

        def label_Sidebar_User_QTime_():
            self.label_Sidebar_User_QTime_N += self.label_Sidebar_User_QTime_B
            if self.label_Sidebar_User_QTime_N > self.label_Sidebar_User_QTime_Stop:
                # 如果没小于终止数值 就运行
                self.label_Sidebar_User.setPixmap(QtGui.QPixmap(":/Gif_User/images/User/"+ str(self.label_Sidebar_User_QTime_N) + ".png"))
                print(":/Gif_User/images/User/"+ str(self.label_Sidebar_User_QTime_N) + ".png")
            else:
                self.label_Sidebar_User_QTime.stop()

        self.label_Sidebar_User_QTime = QTimer()
        self.label_Sidebar_User_QTime.start(30)
        self.label_Sidebar_User_QTime.timeout.connect(label_Sidebar_User_QTime_)

    def RunInitialize(self, First=True):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""
        if First == True:
            self.RunInitialize_.stop()

        # 开始播放动图
        self.Page_Loading = QtGui.QMovie(":/widget_Sidebar/images/MOS_Logo_gif.gif")
        self.label_loading_gif.setMovie(self.Page_Loading)
        self.Page_Loading.start()

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
            self.Page_Loading.stop()

    def FirstStartInitialize(self):
        """在第一次启动时 初始化(缓存)"""
        from Code.Code import InitializeFirst
        InitializeFirst()
        self.Animation_ToMainWindow(HelloToMainLoading=True)

    def FirstStartInitializeOk(self):
        """在第一次启动时 初始化(缓存) 的页面切换动画完成后"""
        self.RunInitialize(First=False)  # 重新读取配置

    def Animation_ToMainWindow(self, HelloToMainLoading=False):
        """
            动画函数-……(默认 加载)页面->主页面

            HelloToMainLoading: 从欢迎页面到加载页面
        """

        # 切换为第……页
        if HelloToMainLoading == False:
            self.Animation_ToMainWindow_Int_Page = 0
        elif HelloToMainLoading:
            # 欢迎页切换为加载页
            self.Animation_ToMainWindow_Int_Page = 1

        # 设置透明度
        self.Opacity = QGraphicsOpacityEffect()  # 透明度对象
        # self.Opacity.setOpacity(1)  # 初始化设置透明度为，即不透明
        # self.label.setGraphicsEffect(self.Opacity)  # 把标签的透明度设置为为self.opacity

        self.Animation_ToMainWindow_Int_Original = 1  # 原来多少
        self.Animation_ToMainWindow_Int = 0.05  # 每次淡出/入多少

        def Animation():
            """淡出"""
            self.Animation_ToMainWindow_Int_Original -= self.Animation_ToMainWindow_Int
            if self.Animation_ToMainWindow_Int_Original < 0:
                self.Animation_ToMainWindow_Run.stop()
                self.stackedWidget_main.setCurrentIndex(self.Animation_ToMainWindow_Int_Page)

                # 初始化淡出
                self.Animation_ToMainWindow_Int_Original = 0  # 原来多少
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
                if HelloToMainLoading == True:
                    # 如果是从欢迎页面渐变的 就重新加载json
                    self.FirstStartInitializeOk()
            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        # 触发切换动画(淡出)
        self.Animation_ToMainWindow_Run = QTimer()
        self.Animation_ToMainWindow_Run.start(1)
        self.Animation_ToMainWindow_Run.timeout.connect(Animation)


class RunInitializeThread(QThread):
    def __init__(self):
        super(RunInitializeThread, self).__init__()

    def run(self) -> None:
        pass


def Run():
    print("程序已开始运行！")
    app = QtWidgets.QApplication(sys.argv)
    print("创建窗口对象成功！")
    ui = RunUi()
    print("创建PyQt窗口对象成功！")
    sys.exit(app.exec())
