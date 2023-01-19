# coding=utf-8

from PyQt6 import QtWidgets, QtCore, QtGui


class MyQWidget(QtWidgets.QFrame):
    # 自定义单击信号
    clicked = QtCore.pyqtSignal()
    mouseEnterEvent = QtCore.pyqtSignal()
    mouseLeaveEvent = QtCore.pyqtSignal()

    def __int__(self):
        super().__init__()

    # 重写单击事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()

    # 重写悬浮事件
    def enterEvent(self, QEvent):
        self.mouseEnterEvent.emit()

    def leaveEvent(self, QEvent):
        self.mouseLeaveEvent.emit()