#-*-coding:utf-8-*-
from requests import get as requests_get
from requests.models import Response as RequestResponse

#Mod类型
ModFilters = ["adventure", "cursed", "decoration", "equipment", "food", "game-mechanics", "library", "magic", "management",
              "minigame", "mobs", "optimization", "storage", "technology", "transportation", "utility", "worldgen"]

#Mod搜索排序方式
#relevance:按匹配度排列
#downloads:按下载量排列
#follows:按浏览量排列
#newest:按Mod发布时间排列
#updated:按Mod最近更新时间排列
ModSearchIndexes = ["relevance", "downloads", "follows", "newest", "updated"]

ModLoaderTypes = ["forge", "fabric"]

#搜索信息类
"""
params:
    Keyword:搜索关键字
    index:排序方式
    Modfilter:Mod类型
    ModLoaderType:Mod加载器类型
    ModMCVersion:指定搜索支持某个MC版本的mod
"""
class SearchInfo:
    def __init__(self, Keyword:str = None, index:str = None, Modfilter:str = None, ModLoaderType:str = None, ModMCVersion:str = None) -> None:
        self.Keyword = Keyword
        self.Index = index
        self.ModFilter = Modfilter
        self.ModLoaderType = ModLoaderType
        self.ModMCVersion = ModMCVersion
        
#真正的搜索类
"""
searchinfo:搜索信息
Return Type:请求api返回的response
"""
def SearchMods(searchinfo:SearchInfo) -> RequestResponse:
    RequestUrl = "https://mcim.z0z0r4.top/modrinth/search?"
    args = []
    if(searchinfo.Keyword is not None):args.append(f"query={searchinfo.Keyword}")
    if(searchinfo.Index is not None):args.append(f"index={searchinfo.Index}")
    if(any([searchinfo.ModFilter, searchinfo.ModLoaderType, searchinfo.ModMCVersion])):
        facetslist = []
        if(searchinfo.ModFilter is not None):facetslist.append([f"categories:{searchinfo.ModFilter}",])
        if(searchinfo.ModLoaderType is not None):facetslist.append([f"categories:{searchinfo.ModLoaderType}",])
        if(searchinfo.ModMCVersion is not None):facetslist.append([f"versions:{searchinfo.ModMCVersion}",])
        facetstr:str = str(facetslist)
        args.append(f"facets={facetstr}")
    RequestUrl += "&".join(args).replace('\'', '\"')
    return requests_get(RequestUrl);
    