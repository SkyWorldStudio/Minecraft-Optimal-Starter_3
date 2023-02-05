import os
import re
import subprocess

# JavaFind:java寻找类
class JavaFinder:
    # Find_By_Classpath:通过环境变量寻找java,通用win和linux
    # return value:元组,(java路径,java版本) or None
    @staticmethod
    def Find_By_Classpath() -> tuple:
        javapath = ""
        javaver = ""
        paths = dict(os.environ)
        if("JAVA_HOME" in paths.keys()): # 通过环境变量JAVA_HOME查找
            javahome = paths["JAVA_HOME"]
            if(os.path.exists(javahome)):
                unixjavapath = os.path.join(javahome, "bin", "java")
                winjavapath = os.path.join(javahome, "bin", "java.exe")
                if(os.path.exists(unixjavapath)):
                    javapath = unixjavapath
                elif(os.path.exists(winjavapath)):
                    javapath = winjavapath
                else:
                    return None
                javaver = JavaFinder.GetJavaVersion(javahome)
        else:
            return None
        return (javapath, javaver)
    
    # GetJavaVersion:通过查看release文件确定java版本
    # return value:str,java版本 or "Unkown"
    @staticmethod
    def GetJavaVersion(javapath:str) -> str:
        releasefile = os.path.join(javapath, "release") # java目录下的release文件存在java信息
        if(os.path.exists(releasefile)):
            f = open(releasefile, "r")
            filecon = f.read()
            result = re.findall("JAVA_VERSION=\"([\\s\\S]+)\"", filecon) # 通过正则匹配文件内容
            if(len(result) != 0):
                return result[0]
            else:
                return "Unkown"
        else:
            return "Unkown"
    
    # Find_By_Command_Linux:通过命令查找java,仅限linux
    # return value:元组,(java路径,java版本) or None
    @staticmethod
    def Find_By_Command_Linux() -> tuple:
        javaver = ""
        result = subprocess.run(["which", "java"], stdout=subprocess.PIPE) # 通过which命令查找java
        output = result.stdout.decode("utf-8")
        if(output is None or output == ""):return None
        if(os.path.exists(output.strip())):
            output = os.path.realpath(output.strip())
            javasp = output.strip().split(os.path.sep)
            javasp = javasp[0:len(javasp)]
            javahome = os.path.sep.join(javasp)
            javahome = os.path.realpath(javahome)
            javaver = JavaFinder.GetJavaVersion(javahome)
            return (javahome, javaver)
        else:return None

    # Find_By_ProgramFile_Win:通过查找Program Files目录寻找java
    # return value:list,[(java路径,java版本), ...] or []
    @staticmethod
    def Find_By_ProgramFile_Win():
        javas = []
        SysDrive = os.getenv("SystemDrive")
        JavaPath = os.path.join(SysDrive, "Program Files", "Java")
        if(os.path.exists(JavaPath) and os.path.isdir(JavaPath)):
            javadirs = os.listdir(JavaPath)
            if(len(javadirs) != 0):
                for i in javadirs:
                    javaabspath = os.path.join(JavaPath, i)
                    javabin = os.path.join(javaabspath, "bin", "java.exe")
                    if(os.path.exists(javabin)): # 通过判断是否存在java.exe判断是不是合法的java目录
                        javaver = JavaFinder.GetJavaVersion(javaabspath)
                        javas.append((javaabspath, javaver))
        return javas
    
    # Find_Linux:在linux下寻找java的总方法
    # return value:元组,(java路径,java版本) or None
    @staticmethod
    def Find_Linux() -> tuple:
        result = JavaFinder.Find_By_Classpath()
        result2 = JavaFinder.Find_By_Command_Linux()
        if(any([result, result2])):
            if(result is None):return result2
            else:return result

    # Find_Linux:在Windows下寻找java的总方法
    # return value:list,[(java路径,java版本), ...] or []
    @staticmethod
    def Find_Windows():
        result = JavaFinder.Find_By_Classpath()
        result2 = JavaFinder.Find_By_ProgramFile_Win()
        if(result is not None or len(result2) > 0):
            if(len(result2) > 0):
                if(result is not None and result in result2):
                    return result2
                elif(result is not None):
                    result2.append(result)
                    return result2
                else:return result2
            else:return [result]
        else:return []

    