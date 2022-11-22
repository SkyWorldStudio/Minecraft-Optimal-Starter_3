# coding=utf-8
from .Code import JsonWrite
from .Log import print_

class GameFile:
    def __init__(self, JsonFile, Json_MOS):
        """
            游戏文件夹操作
            :param JsonFile: Json设置目录
            :param Json_MOS: Json内容
        """
        super(GameFile, self).__init__()
        self.JsonFile = JsonFile
        self.Json_MOS = Json_MOS

    def GameFile_Add(self, Name, File):
        """
            添加游戏文件夹
            :param Name: 名称
            :param File: 路径
            :return: 'OK'
        """
        print_('Info', '游戏文件夹(添加): 添加文件夹 名称: ' + Name + '路径: ' + File)
        self.Json_MOS['GameFile'][Name] = {
            "Name": Name,
            "File": File
        }

        JsonWrite(self.Json_MOS,self.JsonFile)

