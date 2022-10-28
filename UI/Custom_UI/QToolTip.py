# coding=utf-8
from PyQt6.QtCore import QFile, QPropertyAnimation, QTimer, Qt, QPoint, QSize
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel)
import os
from UI.Custom_UI.QToolTip_Qss import Back

class ToolTip(QFrame):

    def __init__(self, text='', parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.__text = text
        self.__duration = 1000
        self.container = QFrame(self)
        self.timer = QTimer(self)

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.label = QLabel(text, self)
        self.ani = QPropertyAnimation(self, b'windowOpacity', self)

        # set layout
        self.layout().setContentsMargins(15, 10, 15, 15)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(10, 7, 10, 7)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # set style
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setDarkTheme(False)
        self.__setQss()

    def text(self):
        return self.__text

    def setText(self, text: str):
        """ set text on tooltip """
        self.__text = text
        self.label.setText(text)
        self.label.adjustSize()
        self.adjustSize()

    def duration(self):
        return self.__duration

    def setDuration(self, duration: int):
        """ set tooltip duration in milliseconds """
        self.__duration = abs(duration)

    def __setQss(self):
        """ set style sheet """
        #file = os.path.join("UI","Custom_UI","QToolTip.qss")
        #with open(file,'r') as f:
        #    self.setStyleSheet(f.read())

        self.setStyleSheet(Back())

        self.label.adjustSize()
        self.adjustSize()

    def setDarkTheme(self, dark=False):
        """ set dark theme """
        self.setProperty('dark', dark)
        self.label.setProperty('dark', dark)
        self.setStyle(QApplication.style())

    def showEvent(self, e):
        self.timer.stop()
        self.timer.start(self.__duration)
        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def adjustPos(self, pos: QPoint, size: QSize):

        MW_X = self.parent.x()  # 获取主窗口X坐标
        MW_Y = self.parent.y()  # 获取主窗口Y坐标

        if MW_X == pos.x():
            # 通过坐标确认是否为左边栏的按钮
            y = pos.y()
            x = pos.x() + 3*size.width()//2 + size.width()//6.3 - self.width() // 2
        else:
            x = pos.x() + size.width()//2 - self.width()//2
            y = pos.y() + self.height() - 35

        # size.width() 为控件宽
        # size.height() 为控件高
        self.move(round(x), round(y))
