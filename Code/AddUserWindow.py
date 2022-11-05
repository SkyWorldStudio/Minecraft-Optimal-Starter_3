# coding=utf-8
from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6.QtGui import QColor

from UI.AddUserWindow.AddUserWindow import Ui_Dialog_AddUserWindows
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QGraphicsBlurEffect


class Dialog_AddUserWindows_(QDialog,Ui_Dialog_AddUserWindows):
    def __init__(self):
        super(Dialog_AddUserWindows_, self).__init__()
        self.setupUi(self)
        self.show()

        self.pushButton_bottom_cancel.clicked.connect(self.pushButton_Cancel_Clicked)

        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2, 3)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(121, 121, 121, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(18) # 阴影圆角
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到窗口中

    def pushButton_Cancel_Clicked(self):
        self.clicked_pushButton_close()

    def clicked_pushButton_close(self):
        self.pushButton_bottom_cancel.setEnabled(False)  # 为了防止重复操作 直接禁用按钮
        self.anim = QPropertyAnimation(self, b"windowOpacity")  # 设置动画对象
        self.anim.setDuration(300)  # 设置动画时长
        self.anim.setStartValue(1)  # 设置初始属性，1.0为不透明
        self.anim.setEndValue(0)  # 设置结束属性，0为完全透明
        self.anim.finished.connect(self.close_)  # 动画结束时，关闭窗口
        self.anim.start()  # 开始动画

    def close_(self):
        self.close()