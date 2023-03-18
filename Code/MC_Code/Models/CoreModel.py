# 该模块为版本json构造的实体类，可用PyJsonEntity转化
class MCVersions:
    def __init__(self) -> None:
        self.latest = LatestVersions()
        self.versions = [MCVersion()]

class LatestVersions:
    def __init__(self) -> None:
        self.release = None
        self.snapshot = None

class MCVersion:
    def __init__(self) -> None:
        self.id = None
        self.type = None
        self.url = None 
        self.time = None
        self.releaseTime = None
        self.sha1 = None

class LocalMCVersionJson:
    def __init__(self) -> None:
        self.arguments = CoreArgumentJson()
        self.assetIndex = CoreAssetIndexJson()
        self.downloads = CoreDownloadsJson()
        self.id = None
        self.javaVersion = CoreJavaVersion()
        self.libraries = [CoreLibraryJson()]
        self.mainClass = None
        self.minecraftArguments = None
        self.releaseTime = None
        self.time = None
        self.type = None

class CoreArgumentJson:
    def __init__(self) -> None:
        self.game = []
        self.jvm = []

class CoreAssetIndexJson:
    def __init__(self) -> None:
        self.id = None
        self.sha1 = None
        self.size = None
        self.totalSize = None
        self.url = None

class CoreDownloadsJson:
    def __init__(self) -> None:
        self.client = CoreDownloadsItemJson()

class CoreDownloadsItemJson:
    def __init__(self) -> None:
        self.sha1 = None
        self.size = None
        self.url = None

class CoreJavaVersion:
    def __init__(self) -> None:
        self.component = None
        self.majorVersion = None

class CoreLibraryJson:
    def __init__(self) -> None:
        self.downloads = CoreLibraryDownloadsJson()
        self.name = None
        self.rules = [CoreLibraryRuleJson()]
        self.checksums = []
        self.clientreq = None
        self.natives = {}

class CoreLibraryDownloadsJson:
    def __init__(self) -> None:
        self.artifact = CoreLibraryDownloadFileJson()
        self.classifiers = None
        

class CoreLibraryDownloadFileJson:
    def __init__(self) -> None:
        self.path = None
        self.sha1 = None
        self.size = None
        self.url = None

class CoreLibraryRuleJson:
    def __init__(self) -> None:
        self.action:str = None
        self.os = {}


# ---- Not Json Classes ----
class LibraryInfo:
    def __init__(self) -> None:
        self.Json = CoreLibraryJson()
        self.url = None
        self.size = None
        self.name = None
        self.path = None
        self.checksum = None
        self.isenable = None
        self.isnative = None