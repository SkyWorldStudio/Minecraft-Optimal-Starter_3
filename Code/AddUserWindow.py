# coding=utf-8
from UI.AddUserWindow.AddUserWindow import Ui_Dialog_AddUserWindows
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QPropertyAnimation

class Dialog_AddUserWindows_(QDialog,Ui_Dialog_AddUserWindows):
    def __init__(self):
        super(Dialog_AddUserWindows_, self).__init__()
        self.setupUi(self)
        self.show()