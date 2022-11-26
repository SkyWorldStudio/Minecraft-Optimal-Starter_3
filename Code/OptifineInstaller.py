#!--coding:utf-8--

import subprocess
import InstallResult

#用于安装Optifine的类
class OptifineInstaller:
    """
    VanilaGameVersionPath:原版游戏文件夹,注意:原版核心不可改名,保留原名
    JavaPath:java路径
    VersionName:安装核心的版本名
    MinecraftRootPath:.minecraft文件夹
    OptifineInstallerPath:Optifine Installer文件路径,也就是Optifine_XXX_HD_U_XXX.jar
    """
    def __init__(self, VanilaGameVersionPath:str, JavaPath:str, VersionName:str, MinecraftRootPath:str, OptifineInstallerPath:str) -> None:
        self.VanilaGameVersionPath = VanilaGameVersionPath
        self.JavaPath = JavaPath
        self.VersionName = VersionName
        self.MinecraftRootPath = MinecraftRootPath
        self.OptifineInstallerPath = OptifineInstallerPath
    
    #开始安装Optifine
    def StartInstall(self) -> InstallResult.InstallResult:
        #构造命令
        Args = f"{self.JavaPath} -cp \"{self.OptifineInstallerPath};optifine-installer.jar\" net.stevexmh.OptifineInstaller \"{self.MinecraftRootPath}\" \"{self.VersionName}\""
        #print(Args)
        #运行安装进程
        result = subprocess.run(Args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        """
        返回一些信息
        InstallResult.InstallResult:
        isSuccess:操作是否成功
        ErrorMessage:错误信息,仅在出现错误时使用
        OtherArgs:要传出去的可能有用的一些东西
        """
        if(result.returncode != 0):
            return InstallResult.InstallResult(False, result.stderr.decode(errors="ingore"), OtherArgs = [result.returncode, result.args, result.stdout.decode(errors="ingore")])
        else:return InstallResult.InstallResult(True, OtherArgs=[result.args, result.stdout.decode(errors="ingore")])
