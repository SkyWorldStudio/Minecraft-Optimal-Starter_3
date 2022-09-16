# coding=utf-8
import os
from sys import platform


def JsonRead(JsonFile):
    """
        读取Json
        JsonFile = Json的目录
    """
    with open(JsonFile,'r',encoding='utf_8') as f:
        r = f.read()
    return r

def JsonFile():
    """获取Json路径"""
    a = File()
    b = os.path.join(a,'MOS.json')
    return b

def InitializeFirst():
    """在第一次运行时，初始化"""
    f = ['Download','Music','Java','Html','Mod','Logs']
    q = File()
    for f_1 in f:
        file = os.path.join(q,f_1)
        os.makedirs(file,exist_ok=True)

    JsonFile_ = JsonFile()
    with open(JsonFile_,'w',encoding='utf-8'):
        pass


def File():
    """获取缓存目录"""
    s = Systeam()
    if s == 'Mac':
        # 获取当前系统用户目录
        UserFile = os.path.expanduser('~')
        file = os.path.join(UserFile,'Documents','.MOS')
    else:
        file = ''
    return file

def Systeam():
    """
        return: Mac Win Linux

        注意：在本项目中 Cygwin系统 算作Win AIX系统 算作Linux

        'win32':Windows
        'cygwin':Windows/Cygwin
        'darwin':macOS
        'aix':AIX
        'linux':Linux
    """
    a = str(platform)
    if a == 'win32' or a == 'cygwin':
        s = 'Win'
        print(a)
    elif a == 'darwin':
        s = 'Mac'
    elif a == 'linux' or a == 'aix':
        s = 'Linux'
    return s
