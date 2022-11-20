# coding=utf-8

from Code.Code import JsonRead, JsonWrite

class UserAdd():
    def __init__(self,JsonFile):
        """
            添加用户
            ======
            JsonFile: Json目录
        """
        super(UserAdd, self).__init__()
        self.JsonFile = JsonFile

    def UserAdd_OffLine(self,User_Name,UUID=None):
        """
            添加离线账户
            =========
            User_Name: 用户名
            UUID: 自定义UUID, 默认值:None

            :return :OK
        """
        J = JsonRead(self.JsonFile)
        J['Users'][User_Name] = {
            'Manner': 'OffLine',
            'User_Name': User_Name,
            'UUID': UUID
        }
        JsonWrite(J, self.JsonFile)

        return "OK"
