# coding=utf-8
import os
import subprocess


def Check():
    """进行便利并且替换"""
    path = os.path.join('UI')
    for path_1 in os.listdir(path):
        # 便利
        path_q = os.path.join(path, path_1)
        if os.path.isdir(path_q):  # 是否为文件夹
            Name = path_1 + '.py'
            path_2 = os.path.join(path_q, Name)
            if os.path.exists(path_2):
                # 如果目录存在
                c = 'cd ' + path_q + ';' + "sed -ie 's/setPointSize/setPixelSize/g' " + Name
                print('开始执行 目录：' + path_2 + '命令：' + c)
                c_r = subprocess.Popen(c, shell=True)
                c_r.wait()
                print('执行完毕')
            else:
                print('目录：' + path_2 + '未找到，已忽略')
        else:
            print('目录：' + path_q + '不是文件夹,忽略')



if __name__ == '__main__':
    Check()