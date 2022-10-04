# coding=utf-8
import os.path
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, QThread, QEvent, QPoint
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect

from UI.Custom_UI.QToolTip import ToolTip
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
        self.Sidebar_Click_Ok = True  # 记录动画是否完成
        self.Sidebar_Click_C = 'Home'  # 彻底完成后……
        self.label_Sidebar_Back.clicked.connect(self.Back_Clicked)
        self.label_Sidebar_User.clicked.connect(self.User_Clicked)
        self.label_Sidebar_Home.clicked.connect(self.Home_Clicked)
        self.label_Sidebar_OnLine.clicked.connect(self.Online_Clicked)
        self.label_Sidebar_Download.clicked.connect(self.Download_Clicked)
        self.label_Sidebar_Settings.clicked.connect(self.Settings_Clicked)

        self._toolTip = ToolTip(parent=self)
        self.label_Sidebar_Back.setToolTipDuration(1000)
        self.label_Sidebar_User.setToolTipDuration(1000)
        self.label_Sidebar_Home.setToolTipDuration(1000)
        self.label_Sidebar_OnLine.setToolTipDuration(1000)
        self.label_Sidebar_Download.setToolTipDuration(1000)
        self.label_Sidebar_Settings.setToolTipDuration(1000)

        self.label_Sidebar_Back.installEventFilter(self)
        self.label_Sidebar_User.installEventFilter(self)
        self.label_Sidebar_Home.installEventFilter(self)
        self.label_Sidebar_OnLine.installEventFilter(self)
        self.label_Sidebar_Download.installEventFilter(self)
        self.label_Sidebar_Settings.installEventFilter(self)

        self._toolTip.hide()

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

    def Sidebar_Clicked(self, Want=None):
        """
            用户点击左边栏按钮后…\n
            Want: 被点击的"按钮"
        """
        def Go():
            """动画开始运行后 初始化"""
            # 线条动画属性

            self.label_Sidebar_QTime_Go_B = -1  # 步长
            self.label_Sidebar_QTime_Go_Start = 30  # 最小(起始数值)
            self.label_Sidebar_QTime_Go_Stop = 0  # 最大(终止数值)

            # ========= #

            self.label_Sidebar_QTime_Back_B = 1  # 步长
            self.label_Sidebar_QTime_Back_Start = 0  # 最小(起始数值)
            self.label_Sidebar_QTime_Back_Stop = 30  # 最大(终止数值)

            # ========== #
            # 背景动画属性

            self.label_Sidebar_B_QTime_Go_Start = 0  # 起始数值
            self.label_Sidebar_B_QTime_Go_Stop = 10  # 终止数值
            self.label_Sidebar_B_QTime_Go_B = 1  # 步长

            # ========== #

            self.label_Sidebar_B_QTime_Back_Start = 10  # 起始数值
            self.label_Sidebar_B_QTime_Back_Stop = 0  # 终止数值
            self.label_Sidebar_B_QTime_Back_B = -1  # 步长

            if self.Sidebar_Click_Ok:
                # 如果上次全运行完了
                self.label_Sidebar_QTime_Ok = False  # 线条动画是否完成
                self.label_Sidebar_B_QTime_Ok = False  # 背景动画是否完成
                self.label_Sidebar_QTime_Go_N = int(self.label_Sidebar_QTime_Go_Start)  # 记录第几(线-去)
                self.label_Sidebar_QTime_Back_N = int(self.label_Sidebar_QTime_Back_Start)  # 记录第几(线-回)
                self.label_Sidebar_B_QTime_Go_N = int(self.label_Sidebar_B_QTime_Go_Start)  # 记录第几(背景-去)
                self.label_Sidebar_B_QTime_Back_N = int(self.label_Sidebar_B_QTime_Back_Start)  # 记录第几(背景-回)

                self.Sidebar_Click_I = str(self.Sidebar_Click_C)  # 正在变回去的(上次点击的)
            else:
                self.Sidebar_Click_I = str(self.Sidebar_Click_)  # 正在变回去的(上次点击的)
                if self.label_Sidebar_QTime_Ok == False:
                    # 如果上次的线条动画没有运行完成
                    pass
                elif self.label_Sidebar_B_QTime_Ok == False:
                    # 如果上次的背景动画没有运行完成
                    pass

        def label_Sidebar_Go_QTime_():
            self.label_Sidebar_QTime_Go_N += self.label_Sidebar_QTime_Go_B
            if self.label_Sidebar_QTime_Go_N > self.label_Sidebar_QTime_Go_Stop:
                # 如果没小于终止数值 就运行
                if Want == 'Home':
                    self.label_Sidebar_Home.setPixmap(
                        QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Download':
                    self.label_Sidebar_Download.setPixmap(
                        QtGui.QPixmap(
                            ":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(
                        QtGui.QPixmap(
                            ":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))

                label_Sidebar_Back_QTime_()

            elif self.label_Sidebar_QTime_Go_N == self.label_Sidebar_QTime_Go_Stop:
                label_Sidebar_Back_QTime_()

            else:
                self.label_Sidebar_QTime_Ok = True
                IfOk()
                self.label_Sidebar_QTime.stop()

        def label_Sidebar_Back_QTime_():
            if self.label_Sidebar_QTime_Back_N <= self.label_Sidebar_QTime_Back_Stop:
                # 如果小于等于终止数值 就运行
                self.label_Sidebar_QTime_Back_N += self.label_Sidebar_QTime_Back_B
                if self.Sidebar_Click_I == 'Home':
                    self.label_Sidebar_Home.setPixmap(
                        QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Download':
                    self.label_Sidebar_Download.setPixmap(QtGui.QPixmap(
                        ":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                elif self.Sidebar_Click_I == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(QtGui.QPixmap(
                        ":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))

            else:
                pass

        def label_Sidebar_B_Go_QTime_():
            self.label_Sidebar_B_QTime_Go_N += self.label_Sidebar_B_QTime_Go_B
            if self.label_Sidebar_B_QTime_Go_N <= self.label_Sidebar_B_QTime_Go_Stop:
                # 如果没小于终止数值 就运行
                if Want == 'Home':
                    self.label_Sidebar_Home.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    print("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    print("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Online':
                    self.label_Sidebar_OnLine.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Download':
                    self.label_Sidebar_Download.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Settings':
                    self.label_Sidebar_Settings.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")

                label_Sidebar_B_Back_QTime_()

            else:
                IfOk()
                self.label_Sidebar_B_QTime_Ok = True
                self.label_Sidebar_B_QTime.stop()
        def label_Sidebar_B_Back_QTime_():
            self.label_Sidebar_B_QTime_Back_N += self.label_Sidebar_B_QTime_Back_B
            if self.label_Sidebar_B_QTime_Back_N >= self.label_Sidebar_B_QTime_Back_Stop:
                # 如果没小于终止数值 就运行
                if self.Sidebar_Click_I == 'Home':
                    self.label_Sidebar_Home.setStyleSheet("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    print("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setStyleSheet("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    print("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setStyleSheet("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Download':
                    self.label_Sidebar_Download.setStyleSheet("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Settings':
                    self.label_Sidebar_Settings.setStyleSheet("background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")

        def IfOk():
            """检查动画是否完全完成"""
            if self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
                # 如果都完成了
                self.Sidebar_Click_Ok = True
                self.Sidebar_Click_I = False  # 正在变回去的
                self.Sidebar_Click_C = str(Want)  # 彻底完成后……


        print("用户点击左边栏按钮")

        if self.Sidebar_Click_Ok:
            Go()
            self.Sidebar_Click_Ok = False
            self.Sidebar_Click_ = str(Want)

            if Want == self.Sidebar_Click_C:
                # 如果用户又点了一次同样的按钮
                self.Sidebar_Click_ = ''
                self.Sidebar_Click_I = ''

            self.label_Sidebar_QTime = QTimer()
            self.label_Sidebar_QTime.start(15)
            self.label_Sidebar_QTime.timeout.connect(label_Sidebar_Go_QTime_)

            self.label_Sidebar_B_QTime = QTimer()
            self.label_Sidebar_B_QTime.start(15)
            self.label_Sidebar_B_QTime.timeout.connect(label_Sidebar_B_Go_QTime_)


    def RunInitialize(self, First=True):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""
        if First == True:
            self.RunInitialize_.stop()

        # 开始播放动图
        self.Page_Loading = QtGui.QMovie(":/widget_Sidebar/images/MOS_Logo_gif.gif")
        self.label_loading_gif.setMovie(self.Page_Loading)
        self.Page_Loading.start()

        self.JsonFile = os.path.join('')
        from Code.Code import JsonRead, JsonFile
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
                    # 不是就播放左边栏动画
                    self.Sidebar_Clicked(Want='Home')
            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        # 触发切换动画(淡出)
        self.Animation_ToMainWindow_Run = QTimer()
        self.Animation_ToMainWindow_Run.start(1)
        self.Animation_ToMainWindow_Run.timeout.connect(Animation)

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            return super().eventFilter(obj, e)

        tip = self._toolTip
        if e.type() == QEvent.Type.Enter:
            tip.setText(obj.toolTip())
            tip.setDuration(obj.toolTipDuration())
            tip.adjustPos(obj.mapToGlobal(QPoint()), obj.size())
            tip.show()
        elif e.type() == QEvent.Type.Leave:
            tip.hide()
        elif e.type() == QEvent.Type.ToolTip:
            return True

        return super().eventFilter(obj, e)

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
