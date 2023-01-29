# coding=utf-8
import webbrowser

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QColor

from UI.AddUserWindow.AddUserWindow import Ui_Dialog_AddUserWindows
from Code.MainWindow import Return_Window_XY
from Code.Log import print_
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QApplication
import UI.Dialog_All_rc

class Dialog_AddUserWindows_(QDialog, Ui_Dialog_AddUserWindows):
    #sinOut_Win_XY = pyqtSignal(int, int)
    sinOut_OK = pyqtSignal()
    sinOut_Cancel = pyqtSignal()
    sinOut_MicrosoftNoUser = pyqtSignal()

    def __init__(self, JsonFile):
        super(Dialog_AddUserWindows_, self).__init__()
        self.setupUi(self)
        #self.show()

        self.JsonFile = JsonFile
        self.Microsoft_L_Code = None

        self.pushButton_bottom_cancel.clicked.connect(self.pushButton_Cancel_Clicked)
        self.pushButton_bottom_cancel_5.clicked.connect(self.pushButton_Cancel_Clicked)
        self.pushButton_OffLine_Advanced.clicked.connect(self.pushButton_OffLine_Advanced_Clicked)
        self.pushButton_bottom_cancel_confirm_Microsoft.clicked.connect(self.Microsoft_L)
        self.pushButton_bottom_cancel_Microsoft.clicked.connect(self.pushButton_Cancel_Clicked)
        self.pushButton_bottom_cancel_confirm.clicked.connect(self.pushButton_Confirm_Clicked)

        self.OffLine_Advanced_Open = False  # 存储现在 离线登陆中的"高级选项"是否打开

        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2, 3)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(121, 121, 121, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(18)  # 阴影圆角
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到窗口中

        self.label_OffLine.clicked.connect(self.label_OffLine_Clicked)
        self.label_Microsoft.clicked.connect(self.label_Microsoft_Clicked)

        self.label_Microsoft_Code.clicked.connect(self.Microsoft_L_Code_Copy)

    def label_OffLine_Clicked(self):
        """用户点击又是那个角的"离线账户"按钮后"""
        self.stackedWidget_main.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        if not self.OffLine_Advanced_Open:
            self.resize(585, 190)
        else:
            self.resize(585, 230)
        self.label_OffLine.setStyleSheet('color: rgb(0, 119, 255);')
        self.label_Microsoft.setStyleSheet('')
        self.label_else.setStyleSheet('')

    def label_Microsoft_Clicked(self):
        """用户点击又是那个角的"微软账户"按钮后"""
        self.stackedWidget_main.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)
        self.resize(585, 263)
        self.label_OffLine.setStyleSheet('')
        self.label_Microsoft.setStyleSheet('color: rgb(0, 119, 255);')
        self.label_else.setStyleSheet('')

    def Microsoft_L(self):
        """用户在微软页面中点击登陆"""
        self.stackedWidget_3.setCurrentIndex(1)

        self.label_Microsoft_Bottom_2_Loading_GIF = QtGui.QMovie(":/image/images/loading_Window.gif")
        self.label_Microsoft_Bottom_2_Loading.setMovie(self.label_Microsoft_Bottom_2_Loading_GIF)
        self.label_Microsoft_Bottom_2_Loading_GIF.start()

        self.Microsoft_L_Thread_Start_ = Microsoft_L_Thread()
        self.Microsoft_L_Thread_Start_.SinOut_Code.connect(self.Microsoft_L_Thread_SinOut_Code)
        self.Microsoft_L_Thread_Start_.SinOut_UserOK.connect(self.Microsoft_L_Thread_SinOut_UserOK)
        self.Microsoft_L_Thread_Start_.SinOut_NoMicrosoft.connect(self.Microsoft_L_Thread_SinOut_NoMicrosoft)
        self.Microsoft_L_Thread_Start_.start()

    def Microsoft_L_Thread_SinOut_Code(self,Code):
        """微软登陆线程返回 设备代码,时间等"""
        self.Microsoft_L_Code = Code[0]
        webbrowser.open(Code[1])
        self.Microsoft_L_Time = round(Code[2]/60)
        self.label_Microsoft_Code.setText(str(Code[0] + '点击复制,' + str(self.Microsoft_L_Time) + '分钟内有效'))
        self.label_Microsoft_Code.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Microsoft_L_Code_Copy()

    def Microsoft_L_Thread_SinOut_UserOK(self):
        """微软登陆线程返回 用户登录完成"""
        self.stackedWidget_widget_page_Microsoft_Top.setCurrentIndex(1)
        self.resize(585, 165)

    def Microsoft_L_Thread_SinOut_NoMicrosoft(self):
        """微软登陆线程返回 账户中没有MC"""
        self.sinOut_MicrosoftNoUser.emit()

    def Microsoft_L_Code_Copy(self):
        if self.Microsoft_L_Code is not None:
            # 实例化剪切板，标签设置为剪切板的文本并显示
            clipboard = QApplication.clipboard()
            clipboard.setText(self.Microsoft_L_Code)
            self.label_Microsoft_Code.setText('复制成功')
            self.label_Microsoft_Code.setEnabled(False)
            def l_t():
                self.label_Microsoft_Code.setEnabled(True)
                self.label_Microsoft_Code.setText(str(self.Microsoft_L_Code) + '点击复制,' + str(self.Microsoft_L_Time) + '分钟内有效')
                self.Microsoft_L__Code_Copy_QTimer.stop()

            self.Microsoft_L__Code_Copy_QTimer = QTimer()
            self.Microsoft_L__Code_Copy_QTimer.start(500)  # 60s一次
            self.Microsoft_L__Code_Copy_QTimer.timeout.connect(l_t)



    def pushButton_OffLine_Advanced_Clicked(self):
        icon = QtGui.QIcon()
        if self.OffLine_Advanced_Open == False:
            self.OffLine_Advanced_Open = True
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/TriangleUpsideDown.png"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.stackedWidget_OffLine_widget_2.setMaximumSize(QtCore.QSize(16777215, 38))
            self.stackedWidget_OffLine_widget_2.setMinimumSize(QtCore.QSize(0, 38))
            self.stackedWidget_OffLine_widget_2.setCurrentIndex(0)
            self.resize(585, 230)
            self.lineEdit_OffLine_Advanced.setEnabled(True)
        else:
            self.OffLine_Advanced_Open = False
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/TriangleUp.png"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.stackedWidget_OffLine_widget_2.setMaximumSize(QtCore.QSize(16777215, 0))
            self.stackedWidget_OffLine_widget_2.setMinimumSize(QtCore.QSize(0, 0))
            self.stackedWidget_OffLine_widget_2.setCurrentIndex(1)
            self.resize(585, 190)
            self.lineEdit_OffLine_Advanced.setEnabled(False)
        self.pushButton_OffLine_Advanced.setIcon(icon)

    def pushButton_Confirm_Clicked(self):
        """点击登陆按钮"""
        if self.stackedWidget_main.currentIndex() == 0:
            # 如果是使用离线登陆
            User_Name = self.lineEdit_OffLine.text()
            if self.lineEdit_OffLine.text() != '':
                from Code.MC_Code.Users import UserAdd
                if self.lineEdit_OffLine_Advanced.text() != '':
                    # 如果填写了 UUID
                    UUID = self.lineEdit_OffLine_Advanced.text()
                else:
                    UUID = None
                R = UserAdd(self.JsonFile).UserAdd_OffLine(User_Name,UUID)
                if R == 'OK':
                    self.sinOut_OK.emit()
                    self.clicked_pushButton_close()  # 关闭窗口

    def pushButton_Cancel_Clicked(self):
        print_('Info','尝试取消')
        try:
            print(0)
            #self.Microsoft_L_Thread_Start_.exec()
            self.Microsoft_L_Thread_Start_.Quit()
            print(1)
            self.Microsoft_L_Thread_Start_.quit()
            print(2)
            self.Microsoft_L_Thread_Start_.requestInterruption()
            print(3)
            #self.Microsoft_L_Thread_Start_.wait()
            print(4)
        except:
            pass
        self.sinOut_Cancel.emit()
        self.clicked_pushButton_close()

    def clicked_pushButton_close(self):
        self.pushButton_bottom_cancel.setEnabled(False)  # 为了防止重复操作 直接禁用按钮
        self.anim = QPropertyAnimation(self, b"windowOpacity")  # 设置动画对象
        self.anim.setDuration(300)  # 设置动画时长
        self.anim.setStartValue(1)  # 设置初始属性，1.0为不透明
        self.anim.setEndValue(0)  # 设置结束属性，0为完全透明
        self.anim.finished.connect(self.close_)  # 动画结束时，关闭窗口
        self.anim.start()  # 开始动画

    def MoveXY(self,x,y):
        x_ = self.x()
        y_ = self.y()
        x_ = x_ + x
        y_ = y_ + y
        self.move(x_,y_)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # 后期这个要加一个判断,如果是在进行登陆操作,esc按键直接忽略
            self.pushButton_Cancel_Clicked()


    #def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #    self.Is_Drag_ = True
    #    self.Mouse_Start_Point_ = a0.globalPosition()  # 获得鼠标的初始位置
    #    self.Window_Start_Point_ = self.frameGeometry().topLeft()  # 获得窗口的初始位置

    #def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
    #    # 判断是否在拖拽移动
    #    if self.Is_Drag_:
    #        # 获得鼠标移动的距离
    #        self.Move_Distance = a0.globalPosition() - self.Mouse_Start_Point_
    #        # 改变窗口的位置
    #        Main_XY = Return_Window_XY()
    #        self.sinOut_Win_XY.emit(
    #            round(Main_XY.x() + self.Move_Distance.x()),
    #            round(Main_XY.y() + self.Move_Distance.y())
    #        )
    #        x_c_m = self.Move_Distance.x()
    #        y_c_m = self.Move_Distance.y()
    #        x = self.Window_Start_Point_.x() + x_c_m
    #        y = self.Window_Start_Point_.y() + y_c_m
    #        self.move(round(x), round(y))

    #def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
    #    # 放下左键即停止移动
    #    if a0.button() == Qt.MouseButton.LeftButton:
    #        self.Is_Drag_ = False

    def close_(self):
        self.close()

class Microsoft_L_Thread(QThread):
    SinOut_Code = pyqtSignal(list)
    SinOut_UserOK = pyqtSignal()
    SinOut_NoMicrosoft = pyqtSignal()
    def __init__(self):
        """微软登陆线程"""
        super(Microsoft_L_Thread, self).__init__()

    def run(self):
        from Code.MC_Code.MicrosoftAuthenticator import MicrosoftAuthenticator
        self.arg1 = MicrosoftAuthenticator('35402e6c-8e66-4bf2-8f9b-a1de642db842')
        self.arg2 = self.arg1.StartDeviceFlowRequest()
        self.SinOut_Code.emit(self.arg2)
        print_('DeBug','[微软登陆]开启设备代码流验证' + str(self.arg2))

        self.arg3 = self.arg1.WaitForUserCompletedAuth()
        self.SinOut_UserOK.emit()
        print_('DeBug','[微软登陆]用户登陆完成：' + str(self.arg3))

        if self.arg3:
            self.arg4 = self.arg1.XBLAuthToken()
            print_('DeBug','[微软登陆]XBL验证结果' + str(self.arg4))

            self.arg5 = self.arg1.XSTSAuthToken(self.arg4["Token"])
            print_('DeBug', '[微软登陆]XSTS验证结果' + str(self.arg5))

            self.arg6 = self.arg1.LoginWithXbox(self.arg5)
            print_('DeBug', '[微软登陆]登录Xbox结果' + str(self.arg6))

            if self.arg6:
                self.arg7 = self.arg1.isTheAccountHasMinecraft(self.arg6["access_token"])
                print_('DeBug', '[微软登陆]账号是否有正版mc' + str(self.arg7))

                self.arg8 = self.arg1.GetPlayerProfile(self.arg6["access_token"])
                print_('DeBug', '[微软登陆]玩家信息: ' + str(self.arg8))

                access_token = self.arg6['access_token']



    def Quit(self):
        self.arg1.Quit()
    