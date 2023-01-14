# coding=utf-8
"""日志系统"""
import datetime

# 日志系统 这个列表是暂存的 主窗口会定时 获取 -> 写入 -> 清空 (全局变量)
r = []


class Print_Colour:
    """
        HEADER:偏粉的紫色(?)
        OKBLUE:蓝色
        OKCYAN:青色
        OKGREEN:绿色
        OKGREEN_2:有下划线的绿色
        WARNING:黄色
        WARNING_2:有下划线的黄色
        FAIL:红色
        FAIL_2:加粗的红色
        FAIL_3:有下划线的红色
        ENDC:正常的黑色
        BOLD:加粗的黑色
        UNDERLINE:有下横线的黑色
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKGREEN_2 = '\033[4;92m'
    WARNING = '\033[93m'
    WARNING_2 = '\033[4;93m'
    FAIL = '\033[91m'
    FAIL_2 = '\033[1;91m'
    FAIL_3 = '\033[4;91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_(Type, Text, Log=True):
    MOS_print = str(Text)
    Time = datetime.datetime.now().strftime('%H:%M:%S.%f')
    if Type == 'Error':
        Tybe_1 = 'ERROR'
        Tybe_2 = Print_Colour.FAIL_3 + Tybe_1 + Print_Colour.ENDC
        # Time_2 = Print_Colour.FAIL_3 + Time + Print_Colour.ENDC
        Time_2 = Time
        left = Print_Colour.FAIL + '[' + Print_Colour.ENDC
        right = Print_Colour.FAIL + ']' + Print_Colour.ENDC
        # p = left + Time_2 + right + left + Tybe_2 + right + Print_Colour.FAIL_2 + MOS_print + Print_Colour.ENDC
        p = '[' + Time_2 + ']' + '[' + Tybe_2 + ']' + Print_Colour.FAIL_2 + MOS_print + Print_Colour.ENDC
        print(p)
        p_1 = Time + Tybe_1 + MOS_print + '\n'

    elif Type == 'Info':
        Tybe_1 = 'INFO'
        left = Print_Colour.ENDC + '[' + Print_Colour.ENDC
        right = Print_Colour.ENDC + ']' + Print_Colour.ENDC
        Tybe_2 = Print_Colour.OKGREEN_2 + 'INFO' + Print_Colour.ENDC
        # Time_2 = Print_Colour.UNDERLINE + Time + Print_Colour.ENDC
        Time_2 = Time
        p = left + Time_2 + right + left + Tybe_2 + right + Print_Colour.ENDC + MOS_print + Print_Colour.ENDC
        print(p)
        p_1 = '[' + Time + '][' + Tybe_1 + ']' + MOS_print + '\n'

    elif Type == 'DeBug':
        Tybe_1 = 'DEBUG'
        left = Print_Colour.ENDC + '[' + Print_Colour.ENDC
        right = Print_Colour.ENDC + ']' + Print_Colour.ENDC
        Tybe_2 = Print_Colour.WARNING_2 + 'DEBUG' + Print_Colour.ENDC
        # Time_2 = Print_Colour.UNDERLINE + Time + Print_Colour.ENDC
        Time_2 = Time
        p = left + Time_2 + right + left + Tybe_2 + right + Print_Colour.ENDC + MOS_print + Print_Colour.ENDC
        print(p)
        p_1 = '[' + Time + '][' + Tybe_1 + ']' + MOS_print + '\n'
    if Log == True:
        global r
        r.append(p_1)


def Log_Return():
    """获取日志"""
    global r
    return r


def Log_Clear():
    """清空日志"""
    global r
    r = []


if __name__ == '__main__':
    r = []
    print_('Error', '1111')
    print_('Info', 'asdasdas')
    print_('BeBug','askdnasnnaksldnklas')
