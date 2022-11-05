# coding=utf-8
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal, QRect
from PyQt6.QtGui import QColor

from UI.AddUserWindow.AddUserWindow import Ui_Dialog_AddUserWindows
from Code.MainWindow import Return_Window_XY
from PyQt6.QtWidgets import QDialog, QGraphicsDropShadowEffect


class Dialog_AddUserWindows_(QDialog,Ui_Dialog_AddUserWindows):
    sinOut_Win_XY = pyqtSignal(int,int)
    def __init__(self):
        super(Dialog_AddUserWindows_, self).__init__()
        self.setupUi(self)
        self.show()

        self.pushButton_bottom_cancel.clicked.connect(self.pushButton_Cancel_Clicked)
        self.pushButton_OffLine_Advanced.clicked.connect(self.pushButton_OffLine_Advanced_Clicked)

        self.OffLine_Advanced_Open = False  # 存储现在 离线登陆中的"高级选项"是否打开

        # 添加阴影
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(2, 3)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(121, 121, 121, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(18) # 阴影圆角
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到窗口中

    def pushButton_OffLine_Advanced_Clicked(self):
        icon = QtGui.QIcon()
        if self.OffLine_Advanced_Open == False:
            self.OffLine_Advanced_Open = True
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/TriangleUpsideDown.png"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.stackedWidget_OffLine_widget_2.setMaximumSize(QtCore.QSize(16777215, 38))
            self.stackedWidget_OffLine_widget_2.setMinimumSize(QtCore.QSize(0, 38))
            self.stackedWidget_OffLine_widget_2.setCurrentIndex(0)
            self.resize(585, 220)
            self.lineEdit_OffLine_Advanced.setEnabled(True)
        else:
            self.OffLine_Advanced_Open = False
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/TriangleUp.png"), QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.stackedWidget_OffLine_widget_2.setMaximumSize(QtCore.QSize(16777215, 0))
            self.stackedWidget_OffLine_widget_2.setMinimumSize(QtCore.QSize(0, 0))
            self.stackedWidget_OffLine_widget_2.setCurrentIndex(1)
            self.resize(585, 180)
            self.lineEdit_OffLine_Advanced.setEnabled(False)
        self.pushButton_OffLine_Advanced.setIcon(icon)

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

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.Is_Drag_ = True
        self.Mouse_Start_Point_ = a0.globalPosition()  # 获得鼠标的初始位置
        self.Window_Start_Point_ = self.frameGeometry().topLeft()  # 获得窗口的初始位置
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # 判断是否在拖拽移动
        if self.Is_Drag_:
            # 获得鼠标移动的距离
            self.Move_Distance = a0.globalPosition() - self.Mouse_Start_Point_
            # 改变窗口的位置
            Main_XY = Return_Window_XY()
            self.sinOut_Win_XY.emit(
                Main_XY.x() + self.Move_Distance.x(),
                Main_XY.y() + self.Move_Distance.y()
            )
            x_c_m = self.Move_Distance.x()
            y_c_m = self.Move_Distance.y()
            x = self.Window_Start_Point_.x() + x_c_m
            y = self.Window_Start_Point_.y() + y_c_m
            self.move(x,y)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # 放下左键即停止移动
        if a0.button() == Qt.MouseButton.LeftButton:
            self.Is_Drag_ = False

    def close_(self):
        self.close()