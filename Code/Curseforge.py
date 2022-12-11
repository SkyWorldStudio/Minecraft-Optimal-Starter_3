#-*-coding:utf-8-*-

from requests import get as requests_get
from requests.models import Response as RequestResponse

#Mod类型字典
ModTypesDict = {"structures" : 409,
                "playerTransport" : 414,
                "cosmetic" : 424,
                "oresaAndresources" : 408,
                "energy" : 417,
                "armorAndtools" : 434,
                "processing" : 413,
                "twitchIntegration" : 4671,
                "mapAndInformation" : 423,
                "automation" : 4843,
                "utility" : 5191,
                "worldGen" : 406,
                "biomes" : 407,
                "Adventure" : 422,
                "energyAndItemTeleport" : 415,
                "magic" : 419,
                "farming" : 416,
                "library" : 421,
                "technology" : 412,
                "mobs" : 411,
                "redstone" : 4558,
                "server" : 435,
                "food" : 436,
                "miscellaneous" : 425,
                "storage" : 420,
                "dimensions" : 410}


#资源类型字典,Curseforge不只有Mod,还有例如世界,插件等资源
ClassIdsDict = {"worlds":17,
                "bukkitPlugins":5,
                "customization":4546,
                "modpacks":4471,
                "resourcepacks":12,
                "addons":4559,
                "mods":6}

#Mod加载器类型
ModLoadTypesDict = {"forge":1, "fabric":4, "quilt":5}

class QueryCurseforge:
    def __init__(self, 
                 searchFilter:str = None,
                 classId:int = -1,
                 categoryid:int = -1,
                 gameVersion:str = None,
                 modLoaderType:int = -1) -> None:
        """
            Curseforge资源搜索
            :param searchFilter:搜索过滤器,也就是关键字
            :param classId:要搜索的资源类型
            :param categoryid:要搜索的资源类型的类型
            :param gameVersion:指定搜索支持某个MC版本的mod
            :param modLoaderType:加载器类型 
        """
        self.SearchFilter = searchFilter
        self.ClassId = classId
        self.CategoryId = categoryid
        self.GameVersion = gameVersion
        self.ModLoaderType = modLoaderType
        
    def Resources(self,apikey:str) -> RequestResponse:
        """
            Curseforge资源查询
            :param apikey:查询需要的APIKey
            :return: 返回一个请求api的response
        """
        requesturl:str = "https://api.curseforge.com/v1/mods/search?gameId=432?"  # 432为Minecraft的gameId
        args = []
        if self.SearchFilter is not None:
            args.append(f"searchFilter={self.SearchFilter}")
        if self.ClassId != -1:
            args.append(f"classId={self.ClassId}")
        if self.CategoryId != -1:
            args.append(f"categoryId={self.CategoryId}")
        if self.GameVersion is not None:
            args.append(f"gameVersion={self.GameVersion}")
        if self.ModLoaderType != -1:
            args.append(f"modLoaderType={self.ModLoaderType}")
        requesturl += "&".join(args)
        return requests_get(requesturl, headers={"x-api-key":apikey})
        
