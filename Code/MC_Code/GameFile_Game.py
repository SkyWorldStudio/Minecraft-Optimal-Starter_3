# coding=utf-8
import json
import os.path


class GameFile_Game:
    def __init__(self):
        """
            有关"游戏目录下的游戏"的操作
        """
        super(GameFile_Game, self).__init__()

    def GameFile_Game_ReturnGames(self, GameFile):
        """
            检测游戏目录下的游戏
            :param GameFile: 游戏文件夹路径
            :return: 游戏列表,以及游戏初步检查结果
            {游戏名:[(目录存在:True | 目录不存在：False | Json完整: True | Json损坏: False]}  注:Json不存在时自动设为Json损坏,如果Jar和Json文件都不存在会自动忽略
        """
        GF_V = os.path.join(GameFile, 'versions')  # .minecraft/versions
        GF_All = {}
        # 遍历文件夹
        if os.path.exists(GF_V) == True and os.path.isdir(GF_V) == True:  # 检查是否存在 并且为文件夹
            for GF_V_G in os.listdir(GF_V):
                # GF_V_G存储游戏目录名称
                GF_V_G_GF = os.path.join(GF_V, GF_V_G)
                if os.path.isdir(GF_V_G_GF):  # 是否为文件夹
                    Jar = GF_V_G + '.jar'
                    Json = GF_V_G + '.json'
                    GF_V_G_GF_Jar = os.path.join(GF_V_G_GF, Jar)
                    GF_V_G_GF_Json = os.path.join(GF_V_G_GF, Json)

                    if os.path.exists(GF_V_G_GF_Jar):  # 目录是否存在
                        Jar_E = True
                        if os.path.exists(GF_V_G_GF_Json):
                            Json_E = True
                            with open(GF_V_G_GF_Json, 'r', encoding='utf_8') as f:
                                try:
                                    Json_N = json.load(f, strict=False)
                                    if Json_N['id'] == GF_V_G:
                                        Json_C = True
                                    else:
                                        Json_C = False
                                except:
                                    Json_C = False
                        else:
                            Json_E = False
                            Json_C = False
                    else:
                        Jar_E = False
                        # 如果不存在就看看有没有Json
                        if os.path.exists(GF_V_G_GF_Json):
                            Json_E = True
                            with open(GF_V_G_GF_Json, 'r', encoding='utf_8') as f:
                                try:
                                    Json_N = json.load(f, strict=False)
                                    if Json_N['id'] == GF_V_G:
                                        Json_C = True
                                    else:
                                        Json_C = False
                                except:
                                    Json_C = False
                        else:
                            Json_E = False
                            Json_C = None

                    # 情况判断
                    if Json_E == False and Jar_E == False:
                        pass
                    else:
                        State = {
                            'Name': GF_V_G,  # 游戏名称
                            'Jar_Exist': Jar_E,  # Jar文件是否存在
                            'Json_Exist': Json_E,  # Json文件是否存在
                            'Json_Check': Json_C  # Json文件的初步检查是否通过
                        }
                        GF_All[GF_V_G] = State

        return GF_All
