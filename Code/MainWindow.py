# coding=utf-8
from datetime import datetime
import os.path
from sys import argv, exit

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, QEvent, QPoint, Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QListWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QWidget, QSpacerItem, QSizePolicy, QLabel, QVBoxLayout
from pytz import timezone

from Code.Log import print_, Log_Clear, Log_Return
from UI.MainWindow.MainWindow import Ui_MainWindow
from Code.Code import JsonRead, JsonFile, Systeam, JsonWrite, File, Json_Cheak


class RunUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RunUi, self).__init__()

        import UI.MainWindow.img_rc
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowType.MacWindowToolBarButtonHint)
        self.show()

        print_('Info', "程序启动(UI显示): 已成功显示窗体")
        self.__init__setAll()
        self.__init__setToolTipDuration()
        self.__init__setShadow()
        self.X_Y_ = self.frameGeometry().topLeft()

        global Win_XY
        Win_XY = self.geometry()

    # 左边栏"按钮"被点击后（槽）
    def Back_Clicked(self):
        # self.Sidebar_Clicked(Want='Back')
        try:
            print_('Info', '返回系统: 开始返回上一个')
            if self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
                if len(self.H_B) > 2:
                    B = self.H_B[-1]
                    if B['Left'] != False:
                        B_1 = B['Index_L']
                        if B_1 == 0:
                            self.Sidebar_Clicked(Want='User', H=False)
                        elif B_1 == 1:
                            self.Sidebar_Clicked(Want='Home', H=False)
                        elif B_1 == 2:
                            self.Sidebar_Clicked(Want='Online', H=False)
                        elif B_1 == 3:
                            self.Sidebar_Clicked(Want='Download', H=False)
                        elif B_1 == 4:
                            self.Sidebar_Clicked(Want='Settings', H=False)
                    if B['Name'] != False:
                        B_1 = B['Index_L']
                        if B_1 == 0:
                            self.Sidebar_Clicked(Want='User', H=False)
                        elif B_1 == 1:
                            self.Sidebar_Clicked(Want='Home', H=False)
                        elif B_1 == 2:
                            self.Sidebar_Clicked(Want='Online', H=False)
                        elif B_1 == 3:
                            self.Sidebar_Clicked(Want='Download', H=False)
                        elif B_1 == 4:
                            self.Sidebar_Clicked(Want='Settings', H=False)
                        B['Name'].setCurrentIndex(B['Index_L'])
                    # B['Name'].setCurrentIndex(B['Index_L'])
                    print_('Info', '返回系统: 返回完成 本次执行配置值: ' + str(self.H_B[-1]))
                    self.H_B.remove(self.H_B[-1])

                elif len(self.H_B) == 2:
                    B = self.H_B[-1]
                    B_1 = B['Index_L']
                    if B['Name'] != False:
                        B['Name'].setCurrentIndex(B['Index_L'])
                    self.Sidebar_Clicked(Want='Home', H=False)
                    print_('Info', '返回系统: 返回完成 本次执行配置值: ' + str(self.H_B[-1]))
                    self.H_B.remove(self.H_B[-1])

                print(self.H_B)

                if len(self.H_B) == 1:
                    self.label_Sidebar_Back.setEnabled(False)
                    print_('Info', '返回系统: 返回失败, 无需返回 已将按钮改为禁用')

        except IndexError:
            pass

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

    def StackedWidget_Main(self):
        """在切换stackedWidget_main_2后"""
        i = self.stackedWidget_main_2.currentIndex()
        if i == 3:
            # 如果切换到了下载页后
            print('knskldnaklsdnaksndlkasdnalskd')
            self.DownloadPage_stackedWidget_GetGameList_()

    def UserPage_Up_AddUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_addUser.setIcon(icon2)

    def UserPage_Up_AddUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_addUser.setIcon(icon2)

        # 显示窗口
        from Code.AddUserWindow import Dialog_AddUserWindows_
        self.Dialog_AddUserWindows_ = Dialog_AddUserWindows_(self.JsonFile)
        self.Dialog_AddUserWindows_.sinOut_Win_XY.connect(self.Window_XY)
        self.Dialog_AddUserWindows_.sinOut_OK.connect(self.AddUserWindow_OK)
        self.Dialog_AddUserWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.Dialog_AddUserWindows_.setWindowFlags(
            Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
            Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
            Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
            Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
            Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
            Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
        )

        self.Dialog_AddUserWindows_.setWindowModality(
            Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
        )

        self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
        self.Dialog_AddUserWindows_.move(
            round(self.MainWindow_xy_size.x() + (self.size().width()/2 - self.Dialog_AddUserWindows_.size().width()/2)),
            round(self.MainWindow_xy_size.y() + (self.size().height()/3)
        ))  # 子界面移动到 居中
        self.UserPage_Up_AddUser()  # 窗口弹出后，主页面不再刷新，所以在窗口弹出前改变

        self.Dialog_AddUserWindows_.show()

    def UserPage_Up_RefreshUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_refreshUser.setIcon(icon2)

    def UserPage_Up_RefreshUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_refreshUser.setIcon(icon2)

    def UserPage_Up_DeleteUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_deleteUser.setIcon(icon2)

    def UserPage_Up_DeleteUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_deleteUser.setIcon(icon2)

    def UserPage_Up_SetChoiceUser(self):
        """账户页 -> 账户列表设置 -> 单/多选"""
        if self.UserPage_setChoice == 'Choice':
            print_('Info', '用户点击: 账户页 -> 账户列表设置 -> 单/多选:设置为多选状态')
            self.UserPage_Up_SetChoiceUser_Set('Choices')
        else:
            print_('Info', '用户点击: 账户页 -> 账户列表设置 -> 单/多选:设置为单选状态')
            self.UserPage_Up_SetChoiceUser_Set('Choice')

    def UserPage_Up_SetChoiceUser_Set(self, a):
        """
            设置"账户"页面的 多选和单选
            a --> 设置为单选还是多选 传入值:'Choice' or' Choices'
        """
        if a == 'Choice':
            # 如果是要设置为单选
            self.UserPage_setChoice = 'Choice'
            self.label_page_users_up_setChoice.setText(
                '<html><head/><body><p><span style=" font-size:16pt;">单选</span>/<span style=" font-size:12pt;">多选</span></p></body></html>')
            self.label_page_users_up_setChoice_icon.setPixmap(
                QtGui.QPixmap(":/widget_Sidebar/images/User_Page_setChoice_Choice.png"))
            self.pushButton_page_users_up_refreshUser.setText('刷新全部')
            self.pushButton_page_users_up_deleteUser.setText('删除全部')
            self.listWidget_users_down.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.Json_MOS['UserPage_setChoice'] = 'Choice'
            JsonWrite(self.Json_MOS, self.JsonFile)

        else:
            # 如果是要设置为多选
            self.UserPage_setChoice = 'Choices'
            self.label_page_users_up_setChoice.setText(
                '<html><head/><body><p><span style=" font-size:16pt;">多选</span>/<span style=" font-size:12pt;">单选</span></p></body></html>')
            self.label_page_users_up_setChoice_icon.setPixmap(
                QtGui.QPixmap(":/widget_Sidebar/images/User_Page_setChoice_Choices.png"))
            self.pushButton_page_users_up_refreshUser.setText('刷新所选')
            self.pushButton_page_users_up_deleteUser.setText('删除所选')
            self.listWidget_users_down.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
            self.Json_MOS['UserPage_setChoice'] = 'Choices'
            JsonWrite(self.Json_MOS, self.JsonFile)

        self.Users_List_Refresh()

    def UserPage_Down_ListWidget_Clicked(self):
        """账户页 -> 账户列表:选择项目"""
        print_('Info', '用户点击: 账户页 -> 账户列表:选择项目')
        if self.UserPage_setChoice == 'Choices':
            item = self.listWidget_users_down.currentItem()
            print(item.text())
            if str(item.checkState()) == 'CheckState.Checked':
                # 如果已经选中
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
            self.listWidget_users_down.editItem(item)

    def MainPage_GameList(self):
        """主页 -> 游戏列表"""
        self.SetCurrentIndex(self.stackedWidget_page_home, 1, 1, True)
        print_('Info', '用户点击: 主页 -> 游戏列表')

    def MainPage_GameList_List_GameFileAdd(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹"""
        self.SetCurrentIndex(self.stackedWidget_page_home, 2, 1, True)
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹')
        self.MainPage_GameList_List_GameFileAdd_Add()

    def MainPage_GameList_List_Refresh(self):
        """
            主页 -> 游戏列表 -> 刷新
        """
        self.listWidget_page_home_game_left.clear()
        self.listWidget_page_home_game_right_gamefile_game.clear()
        self.GameFiles_Read_Thread_Start()

    def MainPage_GameList_List_GameFileAdd_Add(self):
        """
            主页 -> 游戏列表 -> 添加游戏文件夹\n
            主页 -> 游戏列表 -> 添加游戏文件夹 -> 重新选择\n

            弹出选择窗口
        """
        dir = QFileDialog()
        dir.setFileMode(QFileDialog.FileMode.Directory)
        dir.setDirectory(self.File_Parent)
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择窗口:弹出')
        icon = QIcon()
        if dir.exec():
            F = dir.selectedFiles()  # 选择的路径
            print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择目录: ' + str(F[0]))
            self.label_home_game_file_add_file_2.setText(str(F[0]))
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Main_Page_GameFile_AddAgain.png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        else:
            print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择窗口:弹出 -> 取消')
            self.pushButton_game_file_add_again.setText('选择文件夹')
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add.png"),
                            QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_game_file_add_again.setIcon(icon)

    def MainPage_GameList_List_GameFileAdd_TextChanged(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 名称:填写"""
        if self.lineEdit_game_file_add.styleSheet() == "border:2px solid rgb(255, 47, 146);":
            self.lineEdit_game_file_add.setStyleSheet("")

    def MainPage_GameList_List_GameFileAdd_OK(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 确定(保存)"""
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 确定(保存)')
        n = self.lineEdit_game_file_add.text()
        if n  == '':
            self.lineEdit_game_file_add.setStyleSheet("border:2px solid rgb(255, 47, 146);")
        else:
            from Code.MC_Code.GameFile import GameFile
            f = self.label_home_game_file_add_file_2.text()
            a = GameFile(self.JsonFile,self.Json_MOS)
            a.GameFile_Add(n,f)
            print_('Info', '游戏文件夹(添加): 添加文件夹 完成')
            self.stackedWidget_page_home.setCurrentIndex(1)
            self.MainPage_GameList_List_Refresh()  # 刷新
            self.label_home_game_file_add_file_2.setText('请先选择目录')
            self.lineEdit_game_file_add.setText('')



    def MainPage_GameList_List_GameFileAdd_Cancel(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 取消"""
        self.stackedWidget_page_home.setCurrentIndex(1)
        print_('Info','用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 取消')

    def MainPage_GameList_List(self):
        """主页 -> 游戏列表 -> 选中一项"""
        item = self.listWidget_page_home_game_left.currentItem()
        N = item.text()
        # 改变配置文件中的当前选中
        print(self.listWidget_page_home_game_left.currentRow())
        self.Json_MOS['GameFile_List_Clicked'] = int(self.listWidget_page_home_game_left.currentRow())
        JsonWrite(self.Json_MOS,self.JsonFile)

        F = self.Json_MOS['GameFile'][N]['File']
        self.listWidget_page_home_game_right_gamefile_game.clear()
        self.GameFiles_ReturnGameList_Thread_Start(F)

    def DownloadPage_Game_Clicked(self):
        """下载页 -> 游戏本体"""
        if self.stackedWidget_page_download.currentIndex() == 0:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 0, 3, True)

    def DownloadPage_Word_Clicked(self):
        """下载页 -> 游戏本体"""
        if self.stackedWidget_page_download.currentIndex() == 1:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 1, 3, True)

    def DownloadPage_Mode_Clicked(self):
        """下载页 -> 游戏本体"""
        if self.stackedWidget_page_download.currentIndex() == 2:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 2, 3, True)

    def DownloadPage_Conformity_Clicked(self):
        """下载页 -> 游戏本体"""
        if self.stackedWidget_page_download.currentIndex() == 3:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 3, 3, True)

    def DownloadPage_Resource_Clicked(self):
        """下载页 -> 游戏本体"""
        if self.stackedWidget_page_download.currentIndex() == 4:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 4, 3, True)

    def DownloadPage_stackedWidget_setButtonStyleSheet(self,I):
        """
            在下载页面的stackedWidget改变时, 设置 下载页 -> 左上方的按钮控件样式
            :param I : 将下载页面的stackedWidget设置为了第……页
        """
        S = 'border-bottom: 2px solid rgb(0, 119, 225);'
        if I == 0:
            if self.label_page_download_2_game.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet(S)
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')
                self.DownloadPage_stackedWidget_GetGameList_()
        elif I == 1:
            if self.label_page_download_2_word.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet(S)
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 2:
            if self.label_page_download_2_mode.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet(S)
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 3:
            if self.label_page_download_2_conformity.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet(S)
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 4:
            if self.label_page_download_2_resource.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet(S)


    def DownloadPage_stackedWidget_GetGameList_(self):
        """启动多线程请求版本列表"""
        # release: 原版 / Snapshot: 快照版/ old_alpha: 远古版本
        self.label_page_download_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
        self.label_page_download_loading.setMovie(self.label_page_download_loading_)
        self.label_page_download_loading_.start()
        self.stackedWidget_page_download.setCurrentIndex(5)

        if self.checkBox_page_download_mc_official.isChecked() == True:
            self.Download_MC_Kind = 'release'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_Grass.png'
        elif self.checkBox_page_download_mc_test.isChecked() == True:
            self.Download_MC_Kind = 'snapshot'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_CommandBlock.png'
        elif self.checkBox_page_download_mc_previously.isChecked() == True:
            self.Download_MC_Kind = 'old_alpha'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_CraftingTable.png'
        # print(self.File)
        print('lllll')
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_ = DownloadPage_stackedWidget_GetGameList_Thread( 'MCBBS',self.File,self.Download_MC_Kind)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.SinOut.connect(self.DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.SinOut_OK.connect(self.DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_OK)
        self.listWidget_page_1_download.clear()
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.start()

    def DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut(self,name,time):
        """
            得到"多线程请求版本列表"线程输出 并在列表中添加控件
            :param name: 版本名字
            :param time: 发布时间
        """
        item = QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.Download_MC_Kind_IconFile), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        item.setText(name)
        widget = QWidget()
        QVBoxLayout_ = QVBoxLayout()

        l_l = QLabel()
        l_l.setText(name)
        font = QFont()
        font.setPointSize(17)
        l_l.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(l_l.sizePolicy().hasHeightForWidth())
        l_l.setSizePolicy(sizePolicy)


        l_l2 = QLabel()
        l_l2.setText(time)
        font = QFont()
        font.setPointSize(11)
        l_l2.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(l_l2.sizePolicy().hasHeightForWidth())
        l_l2.setSizePolicy(sizePolicy)

        QVBoxLayout_.addWidget(l_l)
        QVBoxLayout_.addWidget(l_l2)
        QVBoxLayout_.setContentsMargins(0, 0, 0, 0)
        QVBoxLayout_.setSpacing(3)

        widget.setLayout(QVBoxLayout_)
        widget.setContentsMargins(0, 0, 0, 0)

        self.listWidget_page_1_download.addItem(item)
        self.listWidget_page_1_download.setItemWidget(item, widget)
    
    def DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_OK(self):
        """
            得到"多线程请求版本列表"线程完成信号
        """
        self.stackedWidget_page_download.setCurrentIndex(0)
        self.label_page_download_loading_.stop()

    def DownloadPage_stackedWidget_GameList_Clicked(self):
        """下载页面 -> 原版下载列表: 点击项目"""
        item = self.listWidget_page_1_download.currentItem()
        t = item.text()
        self.label_page_download_1_install_bottom.setText(str(t) + '安装')
        self.lineEdit_page_download_1_install_bottom_GameName.setPlaceholderText(str(t))
        self.SetCurrentIndex(self.stackedWidget_page_download_1, 1, 3, True)

    def DownloadPage_stackedWidget_install_fabric_list_bata(self):
        """下载页面 -> 选择安装 -> Fabric -> 测试版"""
        if self.widget_page_download_1_install_fabric_list_bata_list.geometry().height() == 0:
            M = 'Go'
        else:
            M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_fabric_list_bata_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        # self.widget_page_download_1_install_fabric_list_bata_list.setMaximumSize(16777215, 16777215)
    def DownloadPage_stackedWidget_install_fabric_list_version(self):
        """下载页面 -> 选择安装 -> Fabric -> 稳定版"""
        if self.widget_page_download_1_install_fabric_list_version_list.geometry().height() == 0:
            M = 'Go'
        else:M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_fabric_list_version_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        # self.widget_page_download_1_install_fabric_list_version_list.setMaximumSize(16777215, 16777215)
    def DownloadPage_stackedWidget_install_fabric(self):
        """下载页面 -> 选择安装 -> Fabric"""
        print('ss')
        print(self.widget_page_download_1_install_fabric_list.geometry().height())
        if self.widget_page_download_1_install_fabric_list.geometry().height() == 0:
            M = 'Go'
        else:M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_fabric_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        # self.widget_page_download_1_install_fabric_list.setMaximumSize(16777215, 16777215)

    def DownloadPage_stackedWidget_install_forge(self):
        """下载页面 -> 选择安装 -> Forge"""
        if self.widget_page_download_1_install_forge_list.geometry().height() == 0:
            M = 'Go'
        else:M = 'Back'
        i = self.listWidget_download_1_install_forge_list.count()
        s = i*28 + i
        print(i)
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_forge_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False,To=s
                                        )
        #self.widget_page_download_1_install_forge_list.setMaximumSize(16777215,16777215)
    def DownloadPage_stackedWidget_install_optifine_list_bata(self):
        """下载页面 -> 选择安装 -> Optifine -> 测试版"""
        if self.widget_page_download_1_install_optifine_list_bata_list.geometry().height() == 0:
            M = 'Go'
        else:M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_optifine_list_bata_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        #self.widget_page_download_1_install_optifine_list_bata_list.setMaximumSize(16777215,16777215)
    def DownloadPage_stackedWidget_install_optifine_list_version(self):
        """下载页面 -> 选择安装 -> Optifine -> 稳定版"""
        if self.widget_page_download_1_install_optifine_list_version_list.geometry().height() == 0:
            M = 'Go'
        else:M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_optifine_list_version_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        #self.widget_page_download_1_install_optifine_list_version_list.setMaximumSize(16777215,16777215)
    def DownloadPage_stackedWidget_install_optifine(self):
        """下载页面 -> 选择安装 -> Optifine"""
        if self.widget_page_download_1_install_optifine_list.geometry().height() == 0:
            M = 'Go'
        else:
            M = 'Back'
        self.DownloadPage_stackedWidget(self.widget_page_download_1_install_optifine_list,
                                        self.scrollArea_page_download_1_install,
                                        M,
                                        False
                                        )
        #self.widget_page_download_1_install_optifine_list.setMaximumSize(16777215,16777215)

    def DownloadPage_MC_Official(self):
        self.checkBox_page_download_mc_test.setChecked(False)
        self.checkBox_page_download_mc_previously.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()
    def DownloadPage_MC_Text(self):
        self.checkBox_page_download_mc_official.setChecked(False)
        self.checkBox_page_download_mc_previously.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()

    def DownloadPage_MC_Previously(self):
        self.checkBox_page_download_mc_official.setChecked(False)
        self.checkBox_page_download_mc_test.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()


    def DownloadPage_stackedWidget_CurrentIndex(self):
        """当下载页面的stackedWidget传来页数改变的信号时 调用DownloadPage_stackedWidget_setButtonStyleSheet"""
        I = self.stackedWidget_page_download.currentIndex()
        print(I)
        if I == 5:
            pass
        else:
            self.DownloadPage_stackedWidget_setButtonStyleSheet(I)

    def SettingsPage_Background_None_Clicked(self):
        """设置页面 -> 背景设置:选择：无"""
        self.MainWinowMainBackground(None)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：无')

    def SettingsPage_Background_1_Clicked(self):
        """设置页面 -> 背景设置:选择：1(清爽橙黄)"""
        self.MainWinowMainBackground(1)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：1(清爽橙黄)')

    def SettingsPage_Background_2_Clicked(self):
        """设置页面 -> 背景设置:选择：2(梦幻浅蓝)"""
        self.MainWinowMainBackground(2)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：2(梦幻浅蓝)')

    def SettingsPage_Background_3_Clicked(self):
        """设置页面 -> 背景设置:选择：3(梦幻浅红)"""
        self.MainWinowMainBackground(3)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：3(梦幻浅红)')

    def SettingsPage_Background_4_Clicked(self):
        """设置页面 -> 背景设置:选择：4(三彩斑斓)"""
        self.MainWinowMainBackground(4)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：4(三彩斑斓)')

    def SettingsPage_Background_5_Clicked(self):
        """设置页面 -> 背景设置:选择：5(蓝白相照)"""
        self.MainWinowMainBackground(5)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：5(蓝白相照)')

    def SettingsPage_Background_6_Clicked(self):
        """设置页面 -> 背景设置:选择：6(深蓝天空)"""
        self.MainWinowMainBackground(6)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：6(深蓝天空)')

    def SettingsPage_Background_7_Clicked(self):
        """设置页面 -> 背景设置:选择：7(粉色迷雾)"""
        self.MainWinowMainBackground(7)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：7(粉色迷雾)')

    def SettingsPage_Sidebar_horizontalSlider(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动"""
        i = self.horizontalSlider_page_settings_sidebar.value()
        i_2 = i * 30
        self.spinBox_page_settings_sidebar.setValue(i)
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2 / 1000) + 's)完成')

    def SettingsPage_Sidebar_horizontalSlider_sliderReleased(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动抬起后"""
        v = self.horizontalSlider_page_settings_sidebar.value()
        self.Json_MOS['Sidebar_Sidebar_Time'] = v
        print_('Info', '用户点击: 设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动抬起/旋转数字输入框    左边栏动画设置值为: ' + str(v))
        JsonWrite(self.Json_MOS, self.JsonFile)

    def SettingsPage_Sidebar_spinBox(self):
        """设置页面 -> 左边栏动画设置 -> 旋转数字输入框"""
        i = self.spinBox_page_settings_sidebar.value()
        self.horizontalSlider_page_settings_sidebar.setValue(i)
        i_2 = i * 30
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2 / 1000) + 's)完成')
        self.SettingsPage_Sidebar_horizontalSlider_sliderReleased()

    def AddUserWindow_OK(self):
        self.Users_List_Refresh()

    def Users_List_Refresh(self):
        """读取账户列表并反馈在控件上"""
        print_('Info', '账户: 刷新账户列表')
        self.Json_MOS = JsonRead(self.JsonFile)  # 重新读取
        U = self.Json_MOS['Users']
        I = -1
        self.listWidget_users_down.clear()
        if U != {}:
            self.stackedWidget_page_users_down.setCurrentIndex(1)

            self.label_users_down_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
            self.label_users_down_loading.setMovie(self.label_users_down_loading_)
            self.label_users_down_loading_.start()

            for U_1 in U:
                I += 1
                User_Name = self.Json_MOS['Users'][U_1]['User_Name']
                F = self.Json_MOS['Users'][U_1]['Manner']
                if F == 'OffLine':
                    # 如果账户是离线账户
                    T = '[离线]' + User_Name
                item = QListWidgetItem(self.listWidget_users_down)
                item.setText(T)
                if self.Json_MOS['UserPage_setChoice'] == 'Choices':
                    # 如果多选开启
                    item.setCheckState(Qt.CheckState.Unchecked)
                self.listWidget_users_down.addItem(item)

            self.label_users_down_loading_.stop()
            self.stackedWidget_page_users_down.setCurrentIndex(0)
        else:
            self.stackedWidget_page_users_down.setCurrentIndex(2)
        print_('Info', '账户: 刷新账户列表完成')

    def MainWinowMainBackground(self, Want, _init_=False):
        """主窗口背景"""
        if Want == None:
            self.centralwidget.setStyleSheet('')
            self.page_main.setStyleSheet(
                '/*模拟阴影*/\n#widget_Middle > #stackedWidget_main_2{border-image: url(:/Scrub/images/Scrub_B2_FFFFFF-50_Main-M-B.png);}')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = False
                JsonWrite(self.Json_MOS, self.JsonFile)
        else:
            self.centralwidget.setStyleSheet(
                '#stackedWidget_main > #page_main{border-image: url(:/BackGround/images/BackGround/' + str(
                    Want) + '.png);}')
            self.page_main.setStyleSheet('')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = Want
                JsonWrite(self.Json_MOS, self.JsonFile)

    def Sidebar_Clicked(self, Want=None, H=True):
        """
            用户点击左边栏按钮后…\n
            Want: 被点击的"按钮" \n
            H: 是否记录历史(True, False)
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
                if len(self.H_B) > 1:
                    self.label_Sidebar_Back.setEnabled(True)
                else:
                    self.label_Sidebar_Back.setEnabled(False)

        def label_Sidebar_Back_QTime_():
            if self.label_Sidebar_QTime_Back_N <= self.label_Sidebar_QTime_Back_Stop:
                # 如果小于等于终止数值 就运行
                self.label_Sidebar_QTime_Back_N += self.label_Sidebar_QTime_Back_B
                if self.Sidebar_Click_I == 'Home':
                    self.label_Sidebar_Home.setPixmap(
                        QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
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
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
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
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
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

        print_('Info', '用户点击: 左边栏按钮 -> ' + str(Want))

        if self.Sidebar_Click_Ok:
            self.label_Sidebar_Back.setEnabled(False)
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
                self.SetCurrentIndex(False, 1, 1, H)
            elif Want == 'User':
                self.SetCurrentIndex(False, 0, 0, H)
            elif Want == 'Online':
                self.SetCurrentIndex(False, 2, 2, H)
            elif Want == 'Download':
                self.SetCurrentIndex(False, 3, 3, H)
            elif Want == 'Settings':
                self.SetCurrentIndex(False, 4, 4, H)

    def DownloadPage_stackedWidget(self, U, U_P, M, S=False, To=None, F=None):
        """
           用户鼠标悬浮/离开下载页面的列表时, 产生动画
           :param U: 要影响的控件
           :param U_P: U的父级(用于获取父级的高)
           :param M: 展开(Go) /收起(Back)
           :param S: 是否开启"减少动画"功能(False True)
           :param F: 运行前对控件(朋友)进行检查(None List), 如果没有完全收缩 ==> 收缩
        """
        self.DownloadPage_stackedWidget_To__ = To
        def Run_Go():
            """动画模块-展开"""
            # print('GO!')
            self.DownloadPage_stackedWidget_J_ += self.DownloadPage_stackedWidget_B_
            if self.DownloadPage_stackedWidget_To_ == -1:
                self.DownloadPage_stackedWidget_Q_ = int(U.geometry().height())
                # print(self.DownloadPage_stackedWidget_Q_)
                if self.DownloadPage_stackedWidget_To__ == None:
                    U.setMaximumSize(16777215, self.DownloadPage_stackedWidget_J_)
                else:
                    print('sadaskdasdajjsjsjsjjjjjjjjjjjjssjsjssssssssssssssssss')
                    U.setMaximumSize(16777215, 8888)
                    U.setMinimumSize(0, 8888)
                # print(self.DownloadPage_stackedWidget_J_)
                self.DownloadPage_stackedWidget_O_ = int(U.geometry().height())
                # print(self.DownloadPage_stackedWidget_O_)
                if self.DownloadPage_stackedWidget_J_ - self.DownloadPage_stackedWidget_O_ != self.DownloadPage_stackedWidget_B_:
                    Stop()

            else:
                if self.DownloadPage_stackedWidget_J_ < self.DownloadPage_stackedWidget_To_:
                    U.setMaximumSize(16777215, self.DownloadPage_stackedWidget_J_)
                elif self.DownloadPage_stackedWidget_J_ == self.DownloadPage_stackedWidget_To_:
                    Stop()
                elif self.DownloadPage_stackedWidget_J_ > self.DownloadPage_stackedWidget_To_:
                    U.setMaximumSize(16777215, self.DownloadPage_stackedWidget_To_)


        def Run_Back():
            """动画模块-收回"""
            U.setMinimumSize(0,0)
            self.DownloadPage_stackedWidget_J_ -= self.DownloadPage_stackedWidget_B_
            if self.DownloadPage_stackedWidget_J_ > self.DownloadPage_stackedWidget_To_:
                U.setMaximumSize(16777215, self.DownloadPage_stackedWidget_J_)
            elif self.DownloadPage_stackedWidget_J_ == self.DownloadPage_stackedWidget_To_:
                U.setMaximumSize(16777215, 0)
                Stop()
            elif self.DownloadPage_stackedWidget_J_ < self.DownloadPage_stackedWidget_To_:
                U.setMaximumSize(16777215, 0)
                Stop()

        def Run_Backs():
            if len(self.DownloadPage_stackedWidget_start_list) != 0:
                print('11111kmsmdksmkmkmmlmlmlmlmlmlmladasdasd')
                for a in self.DownloadPage_stackedWidget_start_list:
                    if len(self.DownloadPage_stackedWidget_start_list) != 0:
                        self.DownloadPage_stackedWidget_J_Backs = int(a.geometry().height())
                        self.DownloadPage_stackedWidget_J_Backs -= self.DownloadPage_stackedWidget_B_
                        if self.DownloadPage_stackedWidget_J_Backs > 0:
                            a.setMaximumSize(16777215, self.DownloadPage_stackedWidget_J_Backs)
                        elif self.DownloadPage_stackedWidget_J_Backs <= 0:
                            a.setMaximumSize(16777215, 0)
                            self.DownloadPage_stackedWidget_start_list.remove(a)
                            print('llllll')
                            print(len(self.DownloadPage_stackedWidget_start_list))
                        print(self.DownloadPage_stackedWidget_start_list)
                    else:
                        print('aaasaaaaaaaaaaaaaaaaaaaa')
                        self.DownloadPage_stackedWidget_QTime_Backs.stop()
                        break
            else:
                self.DownloadPage_stackedWidget_QTime_Backs.stop()

        def Stop():
            self.DownloadPage_stackedWidget_QTime.stop()
            self.DownloadPage_stackedWidget_start = False

        if F != None:
            self.DownloadPage_stackedWidget_start_list = []
            for F_1 in F:
                print(F_1.geometry().height())
                self.DownloadPage_stackedWidget_start_list.append(F_1)
                print(self.DownloadPage_stackedWidget_start_list)


        self.DownloadPage_stackedWidget_time = 0  # 刷新速度
        self.DownloadPage_stackedWidget_From_ = int(U.geometry().height())
        if To == None:
            if M == 'Go':
                if S == False:
                    self.DownloadPage_stackedWidget_To_ = -1  # 当值为-1时，默认直接全展开, 否则会展开到指定的值(减少动画效果的模式下, To_动画展开到str(U_P的高)), 其余部分不需要动画 直接展开)
                else:
                    self.DownloadPage_stackedWidget_To_ = U_P.geometry()
            else:
                self.DownloadPage_stackedWidget_To_ = 0
        else:
            self.DownloadPage_stackedWidget_To_ = To


        self.DownloadPage_stackedWidget_B_ = 15  # 设置步长

        self.DownloadPage_stackedWidget_D_ = int(self.DownloadPage_stackedWidget_From_)  #当前值
        self.DownloadPage_stackedWidget_O_ = int(self.DownloadPage_stackedWidget_From_)  # 设置之后控件实际的值
        self.DownloadPage_stackedWidget_Q_ = int(self.DownloadPage_stackedWidget_From_)  # 设置之前控件实际的值
        self.DownloadPage_stackedWidget_J_ = int(self.DownloadPage_stackedWidget_D_)  # 将要变为

        try:
            self.DownloadPage_stackedWidget_QTime_Backs.stop()
        except AttributeError:
            self.DownloadPage_stackedWidget_start = True

        if F != None and len(self.DownloadPage_stackedWidget_start_list) >= 1:
            self.DownloadPage_stackedWidget_QTime_Backs = QTimer()
            self.DownloadPage_stackedWidget_QTime_Backs.start(self.DownloadPage_stackedWidget_time)
            self.DownloadPage_stackedWidget_QTime_Backs.timeout.connect(Run_Backs)

        self.DownloadPage_stackedWidget_QTime = QTimer()
        self.DownloadPage_stackedWidget_QTime.start(self.DownloadPage_stackedWidget_time)
        if M == 'Go':
            self.DownloadPage_stackedWidget_QTime.timeout.connect(Run_Go)
        else:
            self.DownloadPage_stackedWidget_QTime.timeout.connect(Run_Back)


    def RunInitialize(self, First=True):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""

        def Settings_():
            """设置启动器"""
            # 导入
            # 读取阶段(读取配置等)
            self.Systeam = Systeam()
            print_('Info', '系统检测: 系统：' + self.Systeam)
            self.Json_MOS = JsonRead(self.JsonFile)
            print_('Info', '程序启动(初始化设置): Json读取完成')
            C = Json_Cheak(self.JsonFile)
            if C:
                # 如果返回为True(已补全文件)
                self.Json_MOS = JsonRead(self.JsonFile)
                print_('Info', '程序启动(初始化设置:Json检查): Json不完整, 以补全')
            else:
                print_('Info', '程序启动(初始化设置:Json检查): Json完整')
            print_('Info', '程序启动(初始化设置:Json检查): Json验证完成')
            self.label_loading_text_2.setText('正在设置启动器(4/7)')
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
                self.pushButton_page_users_up_refreshUser.setText('刷新全部')
                self.pushButton_page_users_up_deleteUser.setText('删除全部')

            print_('Info', '程序启动(初始化设置): 设置背景……')
            self.label_loading_text_2.setText('正在设置启动器(5/7)')

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

        # 引用阶段
        print_('Info', '程序启动(初始化设置): 引入库')
        self.label_loading_text_2.setText('正在设置启动器(2/7)')
        import UI.Gif_rc
        import pytz

        # 开始播放动图
        self.Page_Loading = QtGui.QMovie(":/widget_Sidebar/images/MOS_Logo_gif.gif")
        self.label_loading_gif.setMovie(self.Page_Loading)
        self.Page_Loading.start()

        self.JsonFile_Q = os.path.join('')
        self.JsonFile = JsonFile()  # 读取Json路径

        self.File = File()  # 获取缓存目录
        self.File_Parent = os.path.dirname(self.File)  # 缓存目录上一级

        self.H_B = []

        if os.path.isfile(self.JsonFile) == False:
            """如果没有Json这个目录 就转到欢迎(初始化)页面"""
            self.stackedWidget_main.setCurrentIndex(2)
        else:
            # 如果有 就进行下一步
            self.label_loading_text_2.setText('正在设置启动器(3/7)')
            Settings_()

            print_('Info', '程序启动(初始化设置): 读取用户账户')
            self.label_loading_text_2.setText('正在设置启动器(6/7)')
            self.Users_List_Refresh()

            print_('Info', '程序启动(初始化设置): 读取游戏目录列表')
            self.label_loading_text_2.setText('正在设置启动器(7/7)')
            self.GameFiles_Read_Thread_Start()

            print_('Info', '程序启动(初始化设置): 设置完成')
            self.label_loading_text_2.setText('设置完成')
            self.Animation_ToMainWindow()
            self.Page_Loading.stop()  # 暂停动图

            # 设置完成后就运行日志记录程序
            self.Log_QTime = QTimer()
            self.Log_QTime.setInterval(4000)  # 4秒
            self.Log_QTime.timeout.connect(self.Log_QTime_)
            self.Log_QTime.start()

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

    def __init__setAll(self):
        """设置控件信号"""
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

        self.stackedWidget_main_2.currentChanged.connect(self.StackedWidget_Main)

        # 账户页面
        self.pushButton_page_users_up_addUser.clicked.connect(self.UserPage_Up_AddUser)
        self.pushButton_page_users_up_addUser.pressed.connect(self.UserPage_Up_AddUser_Pressed)
        self.pushButton_page_users_up_refreshUser.clicked.connect(self.UserPage_Up_RefreshUser)
        self.pushButton_page_users_up_refreshUser.pressed.connect(self.UserPage_Up_RefreshUser_Pressed)
        self.pushButton_page_users_up_deleteUser.clicked.connect(self.UserPage_Up_DeleteUser)
        self.pushButton_page_users_up_deleteUser.pressed.connect(self.UserPage_Up_DeleteUser_Pressed)
        self.widget_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice_icon.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.listWidget_users_down.itemPressed.connect(self.UserPage_Down_ListWidget_Clicked)

        # 主页
        self.pushButton_page_home_main_game_list.clicked.connect(self.MainPage_GameList)
        # ---> 游戏列表
        self.pushButton_page_home_file_add.clicked.connect(self.MainPage_GameList_List_GameFileAdd)
        self.pushButton_page_home_file_leftrefresh.clicked.connect(self.MainPage_GameList_List_Refresh)
        self.pushButton_game_file_add_again.clicked.connect(self.MainPage_GameList_List_GameFileAdd_Add)
        self.lineEdit_game_file_add.textChanged.connect(self.MainPage_GameList_List_GameFileAdd_TextChanged)
        self.pushButton_game_file_add_ok.clicked.connect(self.MainPage_GameList_List_GameFileAdd_OK)
        self.pushButton_game_file_add_cancel.clicked.connect(self.MainPage_GameList_List_GameFileAdd_Cancel)
        self.listWidget_page_home_game_left.clicked.connect(self.MainPage_GameList_List)

        # 下载页面
        self.label_page_download_2_game.clicked.connect(self.DownloadPage_Game_Clicked)
        self.label_page_download_2_word.clicked.connect(self.DownloadPage_Word_Clicked)
        self.label_page_download_2_mode.clicked.connect(self.DownloadPage_Mode_Clicked)
        self.label_page_download_2_conformity.clicked.connect(self.DownloadPage_Conformity_Clicked)
        self.label_page_download_2_resource.clicked.connect(self.DownloadPage_Resource_Clicked)
        self.stackedWidget_page_download.currentChanged.connect(self.DownloadPage_stackedWidget_CurrentIndex)
        self.checkBox_page_download_mc_official.clicked.connect(self.DownloadPage_MC_Official)
        self.checkBox_page_download_mc_test.clicked.connect(self.DownloadPage_MC_Text)
        self.checkBox_page_download_mc_previously.clicked.connect(self.DownloadPage_MC_Previously)
        self.listWidget_page_1_download.itemPressed.connect(self.DownloadPage_stackedWidget_GameList_Clicked)
        self.widget_page_download_1_install_fabric_list_bata.clicked.connect(self.DownloadPage_stackedWidget_install_fabric_list_bata)
        self.widget_page_download_1_install_fabric_list_version.clicked.connect(self.DownloadPage_stackedWidget_install_fabric_list_version)
        self.widget_page_download_1_install_fabric_up.clicked.connect(self.DownloadPage_stackedWidget_install_fabric)
        self.widget_page_download_1_install_forge_up.clicked.connect(self.DownloadPage_stackedWidget_install_forge)
        self.widget_page_download_1_install_optifine_list_bata.clicked.connect(self.DownloadPage_stackedWidget_install_optifine_list_bata)
        self.widget_page_download_1_install_optifine_list_version.clicked.connect(self.DownloadPage_stackedWidget_install_optifine_list_version)
        self.widget_page_download_1_install_optifine_up.clicked.connect(self.DownloadPage_stackedWidget_install_optifine)

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
        self.horizontalSlider_page_settings_sidebar.sliderPressed.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.horizontalSlider_page_settings_sidebar.sliderReleased.connect(
            self.SettingsPage_Sidebar_horizontalSlider_sliderReleased)
        self.horizontalSlider_page_settings_sidebar.valueChanged.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.spinBox_page_settings_sidebar.valueChanged.connect(self.SettingsPage_Sidebar_spinBox)

    def __init__setShadow(self):
        """设置控件阴影"""
        # 添加阴影
        """
        self.effect_shadow = QGraphicsDropShadowEffect(self.widget_page_users_up)
        self.effect_shadow.setOffset(0, 0)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(225, 225, 225, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(16) # 阴影圆角
        self.widget_page_users_up.setGraphicsEffect(self.effect_shadow)  # 将设置套用
        """

    def __init__setToolTipDuration(self):
        """初始化设置: 设置提示框"""
        # 悬浮提示窗
        from UI.Custom_UI.QToolTip import ToolTip
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
        time_2 = datetime.now(timezone('Etc/GMT-8')).strftime('%Y%m%d')
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

    def SetCurrentIndex(self, U, I, L=False, H=True):
        """
            更改控件的页数，并记录历史
            参数:
                U: 要更改的控件(如果为左边栏请传入False) \n
                I: 要将控件更改为第……页 \n
                L: 是否需要更改左边边栏显示(False, 如果更改->int) \n
                H: 是否记录(True False)
        """
        if H == True and U == False:
            self.H_B.append({
                "Name": U,  # 控件名
                "Index_L": int(self.stackedWidget_main_2.currentIndex()),  # 原来页码
                "Left": L  # 是否更改左边 如果改 值为改为多少 如果不改 值为False
            })
            self.stackedWidget_main_2.setCurrentIndex(I)
        elif H == True and U != False:
            self.H_B.append({
                "Name": U,  # 控件名
                "Index": I,  # 页码
                "Index_L": int(U.currentIndex()),  # 原来页码
                "Left": L,  # 是否更改左边 如果改 值为改为多少 如果不改 值为False
                "Left_L": int(self.stackedWidget_main_2.currentIndex())  # 原来左边页码
            })
            self.stackedWidget_main_2.setCurrentIndex(L)
            U.setCurrentIndex(I)
        if len(self.H_B) > 1 and self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
            self.label_Sidebar_Back.setEnabled(True)
        else:
            self.label_Sidebar_Back.setEnabled(False)
        print(self.H_B)

    def GameFiles_Read_Thread_Start(self):
        """启动游戏目录返回线程 同时启动动画"""
        # 在启动前就检测是不是一个都没有
        if self.Json_MOS['GameFile'] == {}:
            self.stackedWidget_page_home_game_left.setCurrentIndex(1)
        else:
            self.label_page_home_game_left_none_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
            self.label_page_home_game_left_none_loading.setMovie(self.label_page_home_game_left_none_loading_)
            self.label_page_home_game_left_none_loading_.start()
            
            self.listWidget_page_home_game_left.clear()
            
            self.GameFiles_Read_Thread_Start_ = GameFiles_Read_Thread(self.Json_MOS)
            self.GameFiles_Read_Thread_Start_.SinOut.connect(self.GameFiles_Read_Thread_SinOut)
            self.GameFiles_Read_Thread_Start_.SinOutOK.connect(self.GameFiles_Read_Thread_SinOutOK)
            self.GameFiles_Read_Thread_Start_.start()

    def GameFiles_Read_Thread_SinOut(self,N):
        """
            游戏目录返回线程 信号槽
            :param N: 游戏目录名称
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Game_File.png"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        item = QListWidgetItem(icon, N)
        self.listWidget_page_home_game_left.addItem(item)

    def GameFiles_Read_Thread_SinOutOK(self):
        """
            游戏目录返回线程 完成信号
        """
        self.stackedWidget_page_home_game_left.setCurrentIndex(0)
        self.label_page_home_game_left_none_loading_.stop()
        # 设置当前选中
        if self.listWidget_page_home_game_left.count() == 0:
            pass
        else:
            index = self.Json_MOS['GameFile_List_Clicked']
            self.listWidget_page_home_game_left.setCurrentRow(index)
            text_ = self.listWidget_page_home_game_left.item(index)
            text = text_.text()
            GameFile = self.Json_MOS['GameFile'][text]['File']
            self.GameFiles_ReturnGameList_Thread_Start(GameFile)

    def GameFiles_ReturnGameList_Thread_Start(self,GameFile):
        """启动"检测游戏目录下的游戏线程" 同时启动动画"""
        self.GameFiles_ReturnGameList_Thread_Start_ = GameFiles_ReturnGameList_Thread(GameFile)
        self.GameFiles_ReturnGameList_Thread_Start_.SinOut.connect(self.GameFiles_ReturnGameList_Thread_SinOut)
        #self.GameFiles_ReturnGameList_Thread_Start_.SinOutOK.connect(self.GameFiles_Read_Thread_SinOutOK)
        self.GameFiles_ReturnGameList_Thread_Start_.start()

    def GameFiles_ReturnGameList_Thread_SinOut(self,Name):
        """检测游戏目录下的游戏线程 输出处理"""
        item = QListWidgetItem()
        item.setText(Name)
        widget = QWidget()
        hLayout = QHBoxLayout()


        btn_s = QPushButton()  # 设置
        icon_s = QtGui.QIcon()
        icon_s.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Settings_Game.png"), QtGui.QIcon.Mode.Normal,
                         QtGui.QIcon.State.Off)
        btn_s.setIcon(icon_s)
        btn_s.setIconSize(QSize(20, 20))
        btn_s.setMinimumWidth(20)
        btn_s.setMinimumSize(QSize(35, 35))
        btn_s.setMaximumSize(QSize(35, 35))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_s.sizePolicy().hasHeightForWidth())
        btn_s.setSizePolicy(sizePolicy)

        btn_d = QPushButton()  # 删除
        icon_d = QtGui.QIcon()
        icon_d.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete-pressed.png"), QtGui.QIcon.Mode.Normal,
                         QtGui.QIcon.State.Off)
        btn_d.setIcon(icon_d)
        btn_d.setIconSize(QSize(23, 23))
        btn_d.setMinimumWidth(20)
        btn_d.setMinimumSize(QSize(35,35))
        btn_d.setMaximumSize(QSize(35,35))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_d.sizePolicy().hasHeightForWidth())
        btn_d.setSizePolicy(sizePolicy)

        hl = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)  # 水平

        hLayout.addItem(hl)
        hLayout.addWidget(btn_s)
        hLayout.addWidget(btn_d)

        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(5)
        widget.setLayout(hLayout)
        widget.setContentsMargins(0, 0, 0, 0)

        btn_s.clicked.connect(lambda: self.GameFiles_ReturnGameList_Thread_SinOut_PushButton_settings())
        btn_d.clicked.connect(lambda: self.GameFiles_ReturnGameList_Thread_SinOut_PushButton_delate())

        self.listWidget_page_home_game_right_gamefile_game.addItem(item)
        self.listWidget_page_home_game_right_gamefile_game.setItemWidget(item, widget) # 为item设置widget

    def GameFiles_ReturnGameList_Thread_SinOut_PushButton_settings(self):
        """游戏列表设置按钮信号处理"""
        # 获取button
        btn = self.sender()
        # 获取按钮相对于listwwdget的坐标
        # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
        buttonpos = btn.mapToGlobal(QPoint(0, 0)) - self.widget_page_home_game_right.mapToGlobal(QPoint(0, 0))
        # 获取到对象
        item = self.listWidget_page_home_game_right_gamefile_game.indexAt(buttonpos)
        # 获取位置
        index = item.row()
        item_ = self.listWidget_page_home_game_right_gamefile_game.item(index)
        print(item_.text())

    def GameFiles_ReturnGameList_Thread_SinOut_PushButton_delate(self):
        """游戏列表设置按钮信号处理"""
        # 获取button
        btn = self.sender()
        # 获取按钮相对于listwidget的坐标
        # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
        buttonpos = btn.mapToGlobal(QPoint(0, 0)) - self.widget_page_home_game_right.mapToGlobal(QPoint(0, 0))
        # 获取到对象
        item = self.listWidget_page_home_game_right_gamefile_game.indexAt(buttonpos)
        # 获取位置
        index = item.row()
        item_ = self.listWidget_page_home_game_right_gamefile_game.item(index)
        N = item_.text()
        from Code.DelateGameWindow import Dialog_DelateGameWindows_
        gamefile_name = self.listWidget_page_home_game_left.item(self.Json_MOS['GameFile_List_Clicked']).text()
        self.Dialog_DelateGameWindows_ = Dialog_DelateGameWindows_(
            os.path.join(self.Json_MOS['GameFile'][gamefile_name]['File'],'versions'),
            N,
            gamefile_name
        )
        self.Dialog_DelateGameWindows_.sinOut_Win_XY.connect(self.Window_XY)
        self.Dialog_DelateGameWindows_.sinOut_OK.connect(self.AddUserWindow_OK)
        self.Dialog_DelateGameWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.Dialog_DelateGameWindows_.setWindowFlags(
            Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
            Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
            Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
            Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
            Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
            Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
        )

        self.Dialog_DelateGameWindows_.setWindowModality(
            Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
        )

        self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
        self.Dialog_DelateGameWindows_.move(
            round(self.MainWindow_xy_size.x() + (self.size().width()/2 - self.Dialog_DelateGameWindows_.size().width()/2)),
            round(self.MainWindow_xy_size.y() + (self.size().height()/3)
        ))  # 子界面移动到 居中

        self.Dialog_DelateGameWindows_.show()


    def Window_XY(self, X, Y):
        """改变窗口的XY坐标"""
        self.move(round(X), round(Y))

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        global Win_XY
        Win_XY = self.geometry()
        self.Is_Drag_ = True
        self.Mouse_Start_Point_ = a0.globalPosition()  # 获得鼠标的初始位置
        self.Window_Start_Point_ = self.frameGeometry().topLeft()  # 获得窗口的初始位置

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # 判断是否在拖拽移动
        try:
            if self.Is_Drag_:
                # 获得鼠标移动的距离
                self.Move_Distance = a0.globalPosition() - self.Mouse_Start_Point_
                # 改变窗口的位置
                self.move(
                    round(self.Window_Start_Point_.x() + self.Move_Distance.x()),
                    round(self.Window_Start_Point_.y() + self.Move_Distance.y())
                )
        except AttributeError:
            pass

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # 放下左键即停止移动
        if a0.button() == Qt.MouseButton.LeftButton:
            self.Is_Drag_ = False

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


class GameFiles_Read_Thread(QThread):
    SinOut = pyqtSignal(str)
    SinOutOK = pyqtSignal()
    def __init__(self,Json_MOS):
        """
            多线程进行游戏目录读取
            :param Json_MOS: Json内容
        """
        super(GameFiles_Read_Thread, self).__init__()
        self.Json_MOS = Json_MOS
    def run(self):
        # self.Json_MOS = JsonRead(self.JsonFile)
        key_ = self.Json_MOS['GameFile_List']
        for J in key_:
            N = self.Json_MOS['GameFile'][J]['Name']
            F = self.Json_MOS['GameFile'][J]['File']
            self.SinOut.emit(N)

        self.SinOutOK.emit()
        import gc
        del key_,J,N,F
        gc.collect()

class GameFiles_ReturnGameList_Thread(QThread):
    SinOut = pyqtSignal(str)
    def __init__(self,GameFile):
        """
            多线程读取游戏目录下的游戏
            :param GameFile: 游戏目录
        """
        super(GameFiles_ReturnGameList_Thread, self).__init__()
        self.GameFile = GameFile
    def run(self):
        from Code.MC_Code.GameFile_Game import GameFile_Game
        a = GameFile_Game()
        out = a.GameFile_Game_ReturnGames(self.GameFile)
        print(out)
        for game in out:
            if out[game]['Jar_Exist'] == False and out[game]['Json_Check'] == False:
                Z = '缺少Jar文件, 并且Json文件可能已损坏'
            elif out[game]['Jar_Exist'] == False:
                Z = '缺少Jar文件'
            elif out[game]['Json_Exist'] == False:
                Z = '缺少Json文件'
            elif out[game]['Json_Check'] == False:
                Z = 'Json文件可能已损坏'
            else:
                Z = ''
            if Z == '':
                N = out[game]['Name']
            else:
                N = out[game]['Name'] + ' ' + Z
            self.SinOut.emit(N)
        import gc
        del out,a
        gc.collect()

class DownloadPage_stackedWidget_GetGameList_Thread(QThread):
    SinOut = pyqtSignal(str,str)
    SinOut_OK = pyqtSignal()
    def __init__(self,Source,File,Kind):
        """多线程获取版本列表"""
        super(DownloadPage_stackedWidget_GetGameList_Thread, self).__init__()
        self.Source = Source
        self.File = File
        self.Kind = Kind
    def run(self):
        from Code.MC_Code.GamePublishListReturn import GamePublishListReturn
        a = GamePublishListReturn(self.Source,self.File)
        b = a.ListReturn(self.Kind)
        # print(b)
        l = []
        for b_1 in b:
            N = b_1['id']
            T = b_1['time']
            self.SinOut.emit(N,T)
        self.SinOut_OK.emit()
        import gc
        del a,b,l,N,T
        gc.collect()

def Return_Window_XY():
    """返回窗口的坐标"""
    global Win_XY
    return Win_XY


def Run():
    print_('Info', "程序启动(UI显示): 程序已开始运行！")
    app = QtWidgets.QApplication(argv)
    print_('Info', "程序启动(UI显示): 创建窗口对象成功！")
    ui = RunUi()
    print_('Info', "程序启动(UI显示): 创建PyQt窗口对象成功！")
    exit(app.exec())
