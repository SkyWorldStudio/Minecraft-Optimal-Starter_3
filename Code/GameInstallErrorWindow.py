# coding=utf-8
import os.path

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal, QRect
from PyQt6.QtGui import QColor

from UI.GameInstallErrorWindow.GameInstallErrorWindow import Ui_Dialog_GameInstallError
import UI.Dialog_All_rc
from Code.MainWindow import Return_Window_XY
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QApplication


class Dialog_GameInstellErrorWindows_(QDialog, Ui_Dialog_GameInstallError):
    #sinOut_Win_XY = pyqtSignal(int, int)
    sinOut_OK = pyqtSignal()

    def __init__(self, GameName, Game_V,
                 ErrorKind, ErrorCause, ErrorInfo
                 ):
        """
            删除游戏确认
            :param GameName: 游戏名
            :param Game_V: 游戏版本
            :param ErrorKind: 报错关键字（种类）
            :param ErrorCause: 报错原因(str,None)
            :param ErrorInfo: 报错信息(Py的输出)
        """
        super(Dialog_GameInstellErrorWindows_, self).__init__()
        self.setupUi(self)
        self.show()

        self.GameName = GameName
        self.Game_V = Game_V
        self.ErrorKind = ErrorKind
        self.ErrorCause = ErrorCause
        self.ErrorInfo = ErrorInfo

        if self.ErrorCause != None:
            a = '报错原因未知'
        else:
            a = self.ErrorCause

        self.info = '在安装"' + str(self.GameName) + '"(' + str(self.Game_V) + ')' + '时出现错误，部分文件安装/下载失败，'+ a + '\n错误关键字: '+ str(self.ErrorKind) +'\n\n您可以复制详细信息并在关于中进行反馈'
        self.label_3.setText(self.info)

        self.copt_info = '在安装"' + str(self.GameName) + '"(' + str(self.Game_V) + ')' + '时出现错误，部分文件安装/下载失败，'+ a + '\n错误关键字: '+ str(self.ErrorKind) + '\n\n异常输出: \n' + str(self.ErrorInfo) + '\n\n建议在反馈时附带日志文件，您可以在设置中打开日志文件夹'


        self.pushButton_copy.clicked.connect(self.pushButton_Copy_Clicked)
        self.pushButton_ok.clicked.connect(self.pushButton_OK_Clicked)

        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2, 3)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(121, 121, 121, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(18)  # 阴影圆角
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到窗口中


    def pushButton_OK_Clicked(self):
        """点击确定按钮"""
        self.clicked_pushButton_close()  # 关闭窗口

    def pushButton_Copy_Clicked(self):
        """点击复制按钮"""
        # 实例化剪切板，标签设置为剪切板的文本并显示
        clipboard = QApplication.clipboard()
        clipboard.setText(self.copt_info)



    def clicked_pushButton_close(self):
        self.pushButton_ok.setEnabled(False)  # 为了防止重复操作 直接禁用按钮
        self.pushButton_copy.setEnabled(False)  # 为了防止重复操作 直接禁用按钮
        self.anim = QPropertyAnimation(self, b"windowOpacity")  # 设置动画对象
        self.anim.setDuration(300)  # 设置动画时长
        self.anim.setStartValue(1)  # 设置初始属性，1.0为不透明
        self.anim.setEndValue(0)  # 设置结束属性，0为完全透明
        self.anim.finished.connect(self.close_)  # 动画结束时，关闭窗口
        self.anim.start()  # 开始动画

    def MoveXY(self, x, y):
        x_ = self.x()
        y_ = self.y()
        x_ = x_ + x
        y_ = y_ + y
        self.move(x_, y_)

    # def mousePressEvent(self, a0: QtGui.QMouseEvent):
    #    self.Is_Drag_ = True
    #    self.Mouse_Start_Point_ = a0.globalPosition()  # 获得鼠标的初始位置
    #    self.Window_Start_Point_ = self.frameGeometry().topLeft()  # 获得窗口的初始位置

    # def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
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

    # def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
    #    # 放下左键即停止移动
    #    if a0.button() == Qt.MouseButton.LeftButton:
    #        self.Is_Drag_ = False

    def close_(self):
        self.close()
