# coding=utf-8
import datetime
import os.path
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, QThread, QEvent, QPoint
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect

import pytz

from Code.Log import print_,Log_Clear,Log_Return
from UI.Custom_UI.QToolTip import ToolTip
from UI.MainWindow.MainWindow import Ui_MainWindow
from Code.Code import JsonRead, JsonFile, Systeam, JsonWrite, File


class RunUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RunUi, self).__init__()

        import UI.MainWindow.img_rc
        import UI.Gif_rc

        self.setupUi(self)
        self.show()
        print_('Info',"已成功显示窗体")

        self.Log_QTime = QTimer()
        self.Log_QTime.setInterval(2000) # 2秒
        self.Log_QTime.timeout.connect(self.Log_QTime_)
        self.Log_QTime.start()

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

        # 账户页面
        self.pushButton_page_users_up_addUser.clicked.connect(self.UserPage_Up_AddUser)
        self.pushButton_page_users_up_refreshUser.clicked.connect(self.UserPage_Up_RefreshUser)
        self.pushButton_page_users_up_deleteUser.clicked.connect(self.UserPage_Up_DeleteUser)
        self.widget_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice_icon.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)

        # 设置页面
        self.radioButton_settings_background_none.clicked.connect(self.SettingsPage_Background_None_Clicked)
        self.radioButton_settings_background_1.clicked.connect(self.SettingsPage_Background_1_Clicked)
        self.radioButton_settings_background_2.clicked.connect(self.SettingsPage_Background_2_Clicked)
        self.radioButton_settings_background_3.clicked.connect(self.SettingsPage_Background_3_Clicked)
        self.radioButton_settings_background_4.clicked.connect(self.SettingsPage_Background_4_Clicked)
        self.radioButton_settings_background_5.clicked.connect(self.SettingsPage_Background_5_Clicked)
        self.radioButton_settings_background_6.clicked.connect(self.SettingsPage_Background_6_Clicked)
        self.radioButton_settings_background_7.clicked.connect(self.SettingsPage_Background_7_Clicked)

        self.horizontalSlider_page_settings_sidebar.sliderMoved.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.horizontalSlider_page_settings_sidebar.sliderReleased.connect(self.SettingsPage_Sidebar_horizontalSlider_sliderReleased)
        self.spinBox_page_settings_sidebar.valueChanged.connect(self.SettingsPage_Sidebar_spinBox)

        self.__init__setToolTipDuration()

    # 左边栏"按钮"被点击后（槽）
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

    def UserPage_Up_AddUser(self):
        pass
    def UserPage_Up_RefreshUser(self):
        pass
    def UserPage_Up_DeleteUser(self):
        pass
    def UserPage_Up_SetChoiceUser(self):
        if self.UserPage_setChoice == 'Choice':
            self.UserPage_Up_SetChoiceUser_Set('Choices')
        else:
            self.UserPage_Up_SetChoiceUser_Set('Choice')
    def UserPage_Up_SetChoiceUser_Set(self,a):
        """
            设置"账户"页面的 多选和单选
            a --> 设置为单选还是多选 传入值:'Choice' or' Choices'
        """
        if a == 'Choice':
            # 如果是要设置为单选
            self.UserPage_setChoice = 'Choice'
            self.label_page_users_up_setChoice.setText('<html><head/><body><p><span style=" font-size:16pt;">单选</span>/<span style=" font-size:12pt;">多选</span></p></body></html>')
            self.Json_MOS['UserPage_setChoice'] = 'Choice'
            JsonWrite(self.Json_MOS,self.JsonFile)
        else:
            # 如果是要设置为多选
            self.UserPage_setChoice = 'Choices'
            self.label_page_users_up_setChoice.setText('<html><head/><body><p><span style=" font-size:16pt;">多选</span>/<span style=" font-size:12pt;">单选</span></p></body></html>')
            self.Json_MOS['UserPage_setChoice'] = 'Choices'
            JsonWrite(self.Json_MOS,self.JsonFile)

    def SettingsPage_Background_None_Clicked(self):
        """设置页面 -> 背景设置:选择：无"""
        self.MainWinowMainBackground(None)

    def SettingsPage_Background_1_Clicked(self):
        """设置页面 -> 背景设置:选择：1(清爽橙黄)"""
        self.MainWinowMainBackground(1)

    def SettingsPage_Background_2_Clicked(self):
        """设置页面 -> 背景设置:选择：2(梦幻浅蓝)"""
        self.MainWinowMainBackground(2)

    def SettingsPage_Background_3_Clicked(self):
        """设置页面 -> 背景设置:选择：3(梦幻浅红)"""
        self.MainWinowMainBackground(3)

    def SettingsPage_Background_4_Clicked(self):
        """设置页面 -> 背景设置:选择：4(三彩斑斓)"""
        self.MainWinowMainBackground(4)

    def SettingsPage_Background_5_Clicked(self):
        """设置页面 -> 背景设置:选择：5(蓝白相照)"""
        self.MainWinowMainBackground(5)

    def SettingsPage_Background_6_Clicked(self):
        """设置页面 -> 背景设置:选择：6(深蓝天空)"""
        self.MainWinowMainBackground(6)
    def SettingsPage_Background_7_Clicked(self):
        """设置页面 -> 背景设置:选择：7(粉色迷雾)"""
        self.MainWinowMainBackground(7)

    def SettingsPage_Sidebar_horizontalSlider(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动"""
        i = self.horizontalSlider_page_settings_sidebar.value()
        i_2 = i*30
        self.spinBox_page_settings_sidebar.setValue(i)
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2/1000) + 's)完成')

    def SettingsPage_Sidebar_horizontalSlider_sliderReleased(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动抬起后"""
        self.Json_MOS['Sidebar_Sidebar_Time'] = self.horizontalSlider_page_settings_sidebar.value()
        JsonWrite(self.Json_MOS, self.JsonFile)

    def SettingsPage_Sidebar_spinBox(self):
        i = self.spinBox_page_settings_sidebar.value()
        self.horizontalSlider_page_settings_sidebar.setValue(i)
        i_2 = i * 30
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2 / 1000) + 's)完成')
        self.SettingsPage_Sidebar_horizontalSlider_sliderReleased()

    def MainWinowMainBackground(self,Want,_init_=False):
        """主窗口背景"""
        if Want == None:
            self.centralwidget.setStyleSheet('')
            self.page_main.setStyleSheet('/*模拟阴影*/\n#widget_Middle > #stackedWidget_main_2{border-image: url(:/Scrub/images/Scrub_B2_FFFFFF-50_Main-M-B.png);}')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = False
                JsonWrite(self.Json_MOS,self.JsonFile)
        else:
            self.centralwidget.setStyleSheet('#stackedWidget_main > #page_main{border-image: url(:/BackGround/images/BackGround/' + str(Want) + '.png);}')
            self.page_main.setStyleSheet('')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = Want
                JsonWrite(self.Json_MOS, self.JsonFile)



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
                    print_('Info',":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print_('Info',":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    print_('Info',":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
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
                    print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
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
                    self.label_Sidebar_Home.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Download':
                    self.label_Sidebar_Download.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Settings':
                    self.label_Sidebar_Settings.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")

        def IfOk():
            """检查动画是否完全完成"""
            if self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
                # 如果都完成了
                self.Sidebar_Click_Ok = True
                self.Sidebar_Click_I = False  # 正在变回去的
                self.Sidebar_Click_C = str(Want)  # 彻底完成后……

        print_('Info',"用户点击左边栏按钮")

        if self.Sidebar_Click_Ok:
            Go()
            self.Sidebar_Click_Ok = False
            self.Sidebar_Click_ = str(Want)

            if Want == self.Sidebar_Click_C:
                # 如果用户又点了一次同样的按钮
                self.Sidebar_Click_ = ''
                self.Sidebar_Click_I = ''

            Time_ = self.Json_MOS['Sidebar_Sidebar_Time']
            self.label_Sidebar_QTime = QTimer()
            self.label_Sidebar_QTime.start(Time_)
            self.label_Sidebar_QTime.timeout.connect(label_Sidebar_Go_QTime_)

            self.label_Sidebar_B_QTime = QTimer()
            self.label_Sidebar_B_QTime.start(Time_)
            self.label_Sidebar_B_QTime.timeout.connect(label_Sidebar_B_Go_QTime_)

            if Want == 'Home':
                self.stackedWidget_main_2.setCurrentIndex(1)
            elif Want == 'User':
                self.stackedWidget_main_2.setCurrentIndex(0)
            elif Want == 'Online':
                self.stackedWidget_main_2.setCurrentIndex(2)
            elif Want == 'Download':
                self.stackedWidget_main_2.setCurrentIndex(3)
            elif Want == 'Settings':
                self.stackedWidget_main_2.setCurrentIndex(4)

    def RunInitialize(self, First=True):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""

        def Settings_():
            """设置启动器"""
            # 导入
            # 读取阶段(读取配置等)
            self.Systeam = Systeam()
            print_('Info','系统：' + self.Systeam)
            self.Json_MOS = JsonRead(self.JsonFile)
            print_('Info','Json读取完成')
            # 设置阶段
            if self.Systeam != 'Mac':
                self.radioButton_settings_subject_automatic.setEnabled(False)
                self.radioButton_settings_subject_automatic.setToolTip('跟随系统(只限于Mac系统)-当前不可用')

            if self.Json_MOS['Subject'] == 'Light':
                self.radioButton_settings_subject_light.setChecked(True)
            elif self.Json_MOS['Subject'] == 'Dark':
                self.radioButton_settings_subject_dark.setChecked(True)
            elif self.Json_MOS['Subject'] == 'Automatic':
                self.radioButton_settings_subject_automatic.setChecked(True)
            self.horizontalSlider_page_settings_sidebar.setValue(self.Json_MOS['Sidebar_Sidebar_Time'])
            self.spinBox_page_settings_sidebar.setValue(self.Json_MOS['Sidebar_Sidebar_Time'])

            self.UserPage_setChoice = self.Json_MOS['UserPage_setChoice']
            if self.UserPage_setChoice == 'Choice':
                # 如果是单选 就设置为单选
                self.UserPage_Up_SetChoiceUser_Set('Choice')

            print_('Info','设置背景……')
            self.label_loading_text_2.setText('正在设置启动器(3/3)')

            if self.Json_MOS['BackGround'] == False:
                self.MainWinowMainBackground(None)
                self.radioButton_settings_background_none.setChecked(True)
            else:
                self.MainWinowMainBackground(self.Json_MOS['BackGround'], _init_=True)
                if self.Json_MOS['BackGround'] == 1:
                    self.radioButton_settings_background_1.setChecked(True)
                elif self.Json_MOS['BackGround'] == 2:
                    self.radioButton_settings_background_2.setChecked(True)
                elif self.Json_MOS['BackGround'] == 3:
                    self.radioButton_settings_background_3.setChecked(True)
                elif self.Json_MOS['BackGround'] == 4:
                    self.radioButton_settings_background_4.setChecked(True)
                elif self.Json_MOS['BackGround'] == 5:
                    self.radioButton_settings_background_5.setChecked(True)
                elif self.Json_MOS['BackGround'] == 6:
                    self.radioButton_settings_background_6.setChecked(True)
                elif self.Json_MOS['BackGround'] == 7:
                    self.radioButton_settings_background_7.setChecked(True)



        if First == True:
            self.RunInitialize_.stop()


        # 开始播放动图
        self.Page_Loading = QtGui.QMovie(":/widget_Sidebar/images/MOS_Logo_gif.gif")
        self.label_loading_gif.setMovie(self.Page_Loading)
        self.Page_Loading.start()

        self.JsonFile_Q = os.path.join('')
        self.JsonFile = JsonFile()  # 读取Json路径

        self.File = File()  # 获取缓存目录

        if os.path.isfile(self.JsonFile) == False:
            """如果没有Json这个目录 就转到欢迎(初始化)页面"""
            self.stackedWidget_main.setCurrentIndex(2)
        else:
            # 如果有 就进行下一步
            self.label_loading_text_2.setText('正在设置启动器(2/3)')
            Settings_()
            self.label_loading_text_2.setText('设置完成')
            self.Animation_ToMainWindow()
            self.Page_Loading.stop()  # 暂停动图

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


    def __init__setToolTipDuration(self):
        """初始化设置: 设置提示框"""
        # 悬浮提示窗
        self._toolTip = ToolTip(parent=self)
        self.label_Sidebar_Back.setToolTipDuration(1000)
        self.label_Sidebar_User.setToolTipDuration(1000)
        self.label_Sidebar_Home.setToolTipDuration(1000)
        self.label_Sidebar_OnLine.setToolTipDuration(1000)
        self.label_Sidebar_Download.setToolTipDuration(1000)
        self.label_Sidebar_Settings.setToolTipDuration(1000)
        self.radioButton_settings_subject_light.setToolTipDuration(1000)
        self.radioButton_settings_subject_dark.setToolTipDuration(1000)
        self.radioButton_settings_subject_automatic.setToolTipDuration(1000)

        self.label_Sidebar_Back.installEventFilter(self)
        self.label_Sidebar_User.installEventFilter(self)
        self.label_Sidebar_Home.installEventFilter(self)
        self.label_Sidebar_OnLine.installEventFilter(self)
        self.label_Sidebar_Download.installEventFilter(self)
        self.label_Sidebar_Settings.installEventFilter(self)
        self.radioButton_settings_subject_light.installEventFilter(self)
        self.radioButton_settings_subject_dark.installEventFilter(self)
        self.radioButton_settings_subject_automatic.installEventFilter(self)

        self._toolTip.hide()
    
    def Log_QTime_(self):
        """定时将日志写入文件"""
        logs = Log_Return()
        time_2 = datetime.datetime.now(pytz.timezone('Etc/GMT-8')).strftime('%Y%m%d')
        time = time_2 + '.log'
        file = os.path.join(self.File, 'Logs', time)

        if os.path.exists(file):
            with open(file, 'a', encoding='utf-8') as f:
                for log_ in logs:
                    f.write(log_)
        else:
            with open(file, 'w', encoding='utf-8') as f:
                for log_ in logs:
                    f.write(log_)
        Log_Clear()

    def eventFilter(self, obj, e: QEvent):
        """重写 悬浮提示 方法"""
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


def Run():
    print_('Info',"程序已开始运行！")
    app = QtWidgets.QApplication(sys.argv)
    print_('Info',"创建窗口对象成功！")
    ui = RunUi()
    print_('Info',"创建PyQt窗口对象成功！")
    sys.exit(app.exec())
