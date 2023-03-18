import os,sys,platform
# 这里是模块导入需要
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),"../../Models")))
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),"../..")))
from DownloadAPIManager import DownloadAPIManager
from Models import CoreModel

class MCLibrary:
    # GetAllLibrary  获取一个版本json里所有的library信息
    # param GameJsonE:版本json实体
    # result:一个LibraryInfo列表
    '''
    附录:
    LibraryInfo成员:
    - Json:library的原json实体
    - name:library的命名空间
    - path:library json中的path
    - url:library的下载url
    - isenable:该library是否需要在该系统上被下载
    - isnative:该library是不是一个native
    '''
    @staticmethod
    def GetAllLibrary(GameJsonE:CoreModel.LocalMCVersionJson):
        libs:list = []
        for i in GameJsonE.libraries:
            info = CoreModel.LibraryInfo()
            info.Json = i
            info.name = i.name
            if(i.rules is not None):
                info.isenable = MCLibrary.isTheSystemNeedTheLibrary(i)
            if(i.downloads is None):
                if(i.name is None):continue
                info.url = DownloadAPIManager.Current.Libraries.strip('/') + "/" + MCLibrary.GetMavenFilePathFromName(i.name)
                info.path = MCLibrary.GetMavenFilePathFromName(i.name)
                info.isenable = True if i.clientreq is None else i.clientreq
                info.isnative = False
                libs.append(info)
                continue
            if(i.downloads.classifiers is not None):
                info.isnative = True
                info.isenable = MCLibrary.isTheNativeHasTheSysSupport(i)
                if(info.isenable):
                    natkey = i.natives[MCLibrary.GetSysPlatform()].replace(r"${arch}", platform.architecture()[0].strip('bit'))
                    info.name += ":" + natkey
                    nfile = i.downloads.classifiers[natkey]
                    info.size = nfile["size"]
                    info.path = nfile["path"]
                    info.url = nfile["url"]
                    info.checksum = nfile["sha1"]
                libs.append(info)
            elif(i.downloads.artifact is not None):
                info.path = i.downloads.artifact.path
                info.size = i.downloads.artifact.size
                info.checksum = i.downloads.artifact.sha1
                info.url = i.downloads.artifact.url
                info.isnative = False
                info.name = i.name
                libs.append(info)

        return libs
    

    # GetMavenFilePathFromName:从library的命名空间中拼出path
    # param name:library命名空间
    @staticmethod
    def GetMavenFilePathFromName(name:str):
        array = name.split(":")
        namespacepath = array[0].replace('.', os.path.sep)
        packagename = array[1]
        packagever = array[2]
        if(len(array) > 3):
            extarray = array[3:]
            jarname = packagever + "-" + "-".join(extarray)
            return f"{namespacepath}{os.path.sep}{packagename}{os.path.sep}{packagever}{os.path.sep}{packagename}-{jarname}.jar"
        return f"{namespacepath}{os.path.sep}{packagename}{os.path.sep}{packagever}{os.path.sep}{packagename}-{packagever}.jar"
    
    # isTheSystemNeedTheLibrary:判断该系统是否需要该支持库
    # param lib:library实体json
    # result:bool,是否需要
    @staticmethod
    def isTheSystemNeedTheLibrary(lib:CoreModel.CoreLibraryJson):
        windows = unix = macos = False
        for i in lib.rules:
            if(i.os is None):
                windows = unix = macos = True if i.action == "allow" else False
            else:
                for os in i.os.items():
                    if(os[1] == "windows"):
                        windows = True if i.action == "allow" else False
                    elif(os[1] == "linux"):
                        unix = True if i.action == "allow" else False
                    elif(os[1] == "osx"):
                        macos = True if i.action == "allow" else False
        if(sys.platform == "win32"):return windows
        elif(sys.platform == "linux"):return unix
        elif(sys.platform == "darwin"):return macos
        return False

    # isTheNativeHasTheSysSupport 用于判断该native是否有该系统需要的版本
    # lib:library 实体json
    # result:bool,是否有
    @staticmethod
    def isTheNativeHasTheSysSupport(lib:CoreModel.CoreLibraryJson):
        return MCLibrary.GetSysPlatform() in lib.natives

    # GetSysPlatform:获取系统平台名
    def GetSysPlatform():
        if(sys.platform == "win32"):return "windows"
        elif(sys.platform == "linux"):return "linux"
        elif(sys.platform == "darwin"):return "osx"