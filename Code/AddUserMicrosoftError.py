# coding=utf-8
import os.path

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal, QRect
from PyQt6.QtGui import QColor

from Code.Log import print_
from UI.AddUserWindow.AddUserMicrosoftError import Ui_Dialog_AddUserMicrosoftError
import UI.Dialog_All_rc
from Code.MainWindow import Return_Window_XY
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QApplication


class Dialog_AddUserMicrosoftErrorWindow_(QDialog, Ui_Dialog_AddUserMicrosoftError):
    sinOut_OK = pyqtSignal()

    def __init__(self, ErrorKind, ErrorCause, ErrorInfo):
        """
            微软登陆出错
            :param ErrorKind: 报错关键字（种类）
            :param ErrorCause: 报错原因(str,None)
            :param ErrorInfo: 报错信息(Py的输出)
        """
        super(Dialog_AddUserMicrosoftErrorWindow_, self).__init__()
        self.setupUi(self)
        #self.show()

        self.ErrorKind = ErrorKind
        self.ErrorCause = ErrorCause
        self.ErrorInfo = ErrorInfo

        if self.ErrorCause == 'None':
            a = '报错原因未知'
        else:
            a = '可能是由于您' + self.ErrorCause + '所导致的。'

        self.info = '在进行微软登陆时出现错误, '+ a + '\n错误关键字: \n'+ str(self.ErrorKind) +'\n\n您可以复制详细信息并在关于中进行反馈'
        self.label_h1.setText(self.info)

        self.copt_info = '在进行微软登陆时出现错误, '+ a + '\n错误关键字: \n'+ str(self.ErrorKind) + '\n\n异常输出: \n' + str(self.ErrorInfo) + '\n\n建议在反馈时附带日志文件，您可以在设置中打开日志文件夹'
        print_('Error',self.copt_info)


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
        self.sinOut_OK.emit()
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clicked_pushButton_close()

    def close_(self):
        self.close()
