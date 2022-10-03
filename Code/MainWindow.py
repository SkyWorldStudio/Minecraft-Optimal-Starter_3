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

        # 左边栏
        self.Sidebar_Click_ = ''  # 当前点击的控件
        self.label_Sidebar_User.clicked.connect(self.User_Clicked)
        self.label_Sidebar_Back.clicked.connect(self.Back_Clicked)
        self.label_Sidebar_Home.clicked.connect(self.Home_Clicked)
        self.label_Sidebar_Download.clicked.connect(self.Download_Clicked)
        self.label_Sidebar_OnLine.clicked.connect(self.Online_Clicked)
        self.label_Sidebar_Settings.clicked.connect(self.Settings_Clicked)


    def Back_Clicked(self):
        self.Sidebar_Clicked(Want='Back')

    def User_Clicked(self):
        self.Sidebar_Clicked(Want='User')

    def Home_Clicked(self):
        self.Sidebar_Clicked(Want='Home')

    def Online_Clicked(self):
        self.Sidebar_Clicked(Want='Online')

    def Download_Clicked(self):
        self.Sidebar_Clicked(Want='Download')

    def Settings_Clicked(self):
        self.Sidebar_Clicked(Want='Settings')

    def Sidebar_Clicked(self,Want=None):
        """
            用户点击左边栏按钮后…\n
            Want: 被点击的"按钮"
        """
        print("用户点击左边栏按钮")

        self.label_Sidebar_QTime_Go_B = -1  # 步长
        self.label_Sidebar_QTime_Go_Start = 30  # 最小(起始数值)
        self.label_Sidebar_QTime_Go_Stop = 0  # 最大(终止数值)
        self.label_Sidebar_QTime_Go_N = int(self.label_Sidebar_QTime_Go_Start)  # 记录第几

        # ========= #

        self.label_Sidebar_QTime_Back_B = 1  # 步长
        self.label_Sidebar_QTime_Back_Start = 0  # 最小(起始数值)
        self.label_Sidebar_QTime_Back_Stop = 30  # 最大(终止数值)
        self.label_Sidebar_QTime_Back_N = int(self.label_Sidebar_QTime_Back_Start)  # 记录第几

        def label_Sidebar_Go_QTime_():
            self.label_Sidebar_QTime_Go_N += self.label_Sidebar_QTime_Go_B
            if self.label_Sidebar_QTime_Go_N > self.label_Sidebar_QTime_Go_Stop:
                # 如果没小于终止数值 就运行
                if Want == 'Home':
                    self.label_Sidebar_Home.setPixmap(QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'User':
                    self.label_Sidebar_User.setPixmap(QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Download':
                    self.label_Sidebar_Download.setPixmap(QtGui.QPixmap(":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(QtGui.QPixmap(":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))

                label_Sidebar_Back_QTime_()

            elif self.label_Sidebar_QTime_Go_N == self.label_Sidebar_QTime_Go_Stop:
                label_Sidebar_Back_QTime_()

            else:
                self.Sidebar_Click_ = str(Want)
                self.label_Sidebar_QTime.stop()

        def label_Sidebar_Back_QTime_():
            if self.label_Sidebar_QTime_Back_N <= self.label_Sidebar_QTime_Back_Stop:
                # 如果小于等于终止数值 就运行
                self.label_Sidebar_QTime_Back_N += self.label_Sidebar_QTime_Back_B
                if self.Sidebar_Click_ == 'Home':
                    self.label_Sidebar_Home.setPixmap(QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_ == 'User':
                    self.label_Sidebar_User.setPixmap(QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_ == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_ == 'Download':
                    self.label_Sidebar_Download.setPixmap(QtGui.QPixmap(":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                elif self.Sidebar_Click_ == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(QtGui.QPixmap(":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))

            else:
                pass

        if Want == self.Sidebar_Click_:
            # 如果用户又点了一次同样的按钮
            self.Sidebar_Click_ = ''

        self.label_Sidebar_QTime = QTimer()
        self.label_Sidebar_QTime.start(30)
        self.label_Sidebar_QTime.timeout.connect(label_Sidebar_Go_QTime_)

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
