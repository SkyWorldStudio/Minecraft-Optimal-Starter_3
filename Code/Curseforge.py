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

#查询信息类
"""
params:
    searchFilter:搜索过滤器,也就是关键字
    classId:要搜索的资源类型
    categoryid:要搜索的资源类型的类型
    gameVersion:指定搜索支持某个MC版本的mod
    modLoaderType:加载器类型 
"""
class CurseforgeQueryInfo:
    def __init__(self, 
                 searchFilter:str = None,
                 classId:int = -1,
                 categoryid:int = -1,
                 gameVersion:str = None,
                 modLoaderType:int = -1) -> None:
        self.SearchFilter = searchFilter
        self.ClassId = classId
        self.CategoryId = categoryid
        self.GameVersion = gameVersion
        self.ModLoaderType = modLoaderType
        
#真正的查询类
"""
params:
    apikey:查询需要的APIKey,这个是必须的
    queryinfo:查询信息类
ReturnType:返回一个请求api的response
"""
def QueryCurseforgeResources(apikey:str, queryinfo:CurseforgeQueryInfo) -> RequestResponse:
    requesturl:str = "https://api.curseforge.com/v1/mods/search?gameId=432?" #432为Minecraft的gameId
    args = []
    if(queryinfo.SearchFilter is not None):args.append(f"searchFilter={queryinfo.SearchFilter}")
    if(queryinfo.ClassId != -1):args.append(f"classId={queryinfo.ClassId}")
    if(queryinfo.CategoryId != -1):args.append(f"categoryId={queryinfo.CategoryId}")
    if(queryinfo.GameVersion is not None):args.append(f"gameVersion={queryinfo.GameVersion}")
    if(queryinfo.ModLoaderType != -1):args.append(f"modLoaderType={queryinfo.ModLoaderType}")
    requesturl += "&".join(args)
    return requests_get(requesturl, headers={"x-api-key":apikey})
    
