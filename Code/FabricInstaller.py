#!--coding:utf-8--

import json
import os
import time

#Fabric安装类
class FabricInstaller:
    """
    FabricJson:反序列化后的FabricJson, 在https://meta.fabricmc.net/v2/versions/loader/可以获取到
    VanilaCoreJson:反序列化后的原版核心json
    VersionName:欲安装版本名
    MinecraftRootDir:.minecraft路径
    """
    def __init__(self, FabricJson:dict, VanilaCoreJson:dict, VersionName:str, MinecraftRootDir:str) -> None:
        self.FabricJson = FabricJson
        self.VanilaCoreJson = VanilaCoreJson
        self.VersionName = VersionName
        self.MinecraftRootDir = MinecraftRootDir
    
    """
    开始安装
    此函数无参数,无返回值,报错会直接raise出去
    """
    def StartInstall(self):
        #对json信息进行一些构造
        versionjson = self.VanilaCoreJson.copy()
        versionjson["id"] = self.VersionName
        versionjson["inheritsFrom"] = self.VanilaCoreJson["id"]
        versionjson["time"] = versionjson["releaseTime"] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        versionjson["type"] = "release"
        #判断主类是否为None或空字符串并写入
        if(type(self.FabricJson["launcherMeta"].get("mainClass")) == dict):
            versionjson["mainClass"] = self.FabricJson["launcherMeta"]["mainClass"]["client"]
        else:
            if(self.FabricJson["launcherMeta"].get("mainClass") is None or self.FabricJson["launcherMeta"].get("mainClass") == ""):
                versionjson["mainClass"] = "net.minecraft.client.main.Main"
            else:versionjson["mainClass"] = self.FabricJson["launcherMeta"].get("mainClass")
        if(versionjson["mainClass"] == "net.minecraft.client.main.Main"):raise Exception("无法解析主类")
        #合并支持库
        versionjson["libraries"] += self.FabricJson["launcherMeta"]["libraries"]["client"] + self.FabricJson["launcherMeta"]["libraries"]["common"]
        versionpath = os.path.join(self.MinecraftRootDir, "versions", self.VersionName)
        #创建文件夹,写入文件
        jsonpath = os.path.join(versionpath, self.VersionName + ".json").rstrip('/')
        if(os.path.exists(versionpath) is False):os.mkdir(versionpath)
        with open(jsonpath, "w") as f:
            f.write(json.dumps(versionjson, ensure_ascii=False))
        