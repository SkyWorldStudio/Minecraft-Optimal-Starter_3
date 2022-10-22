# coding=utf-8

from PyQt6 import QtWidgets, QtCore, QtGui


class MyQWidget(QtWidgets.QLabel):
    # 自定义单击信号
    clicked = QtCore.pyqtSignal()

    def __int__(self):
        super().__init__()

    # 重写单击事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()