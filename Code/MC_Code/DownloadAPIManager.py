class DownloadAPIRoot:
    def __init__(self) -> None:
        self.VersionManifest:str = None
        self.Libraries:str = None
        self.CoreJar:str = None
        self.CoreJson:str = None
        self.Assets:str = None
        self.AssetIndex:str = None


class DownloadAPIManager:
    Bmclapi = DownloadAPIRoot()
    Mcbbs = DownloadAPIRoot()
    Raw = DownloadAPIRoot()
    # Bmclapi Start
    Bmclapi.AssetIndex = "bmclapi2.bangbang93.com"
    Bmclapi.Assets = "https://bmclapi2.bangbang93.com/assets/"
    Bmclapi.CoreJar = "https://bmclapi2.bangbang93.com/version/<version>/client"
    Bmclapi.CoreJson = "https://bmclapi2.bangbang93.com/version/<version>/json"
    Bmclapi.Libraries = "https://bmclapi2.bangbang93.com/maven"
    Bmclapi.VersionManifest = "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"
    # Mcbbs Start
    Mcbbs.AssetIndex = "download.mcbbs.net"
    Mcbbs.Assets = "https://download.mcbbs.net/assets/"
    Mcbbs.CoreJar = "https://download.mcbbs.net/version/<version>/client"
    Mcbbs.CoreJson = "https://download.mcbbs.net/version/<version>/json"
    Mcbbs.VersionManifest = "https://download.mcbbs.net/mc/game/version_manifest_v2.json"
    Mcbbs.Libraries = "https://download.mcbbs.net/maven"
    # Raw Start
    Raw.VersionManifest = "http://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
    Raw.Libraries = "https://libraries.minecraft.net"
    Raw.Assets = "http://resources.download.minecraft.net"
    # Current
    Current:DownloadAPIRoot = None

