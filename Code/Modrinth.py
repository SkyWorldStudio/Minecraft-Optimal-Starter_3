#-*-coding:utf-8-*-
from requests import get as requests_get
from requests.models import Response as RequestResponse

#Mod类型
ModFilters = ["adventure", "cursed", "decoration", "equipment", "food", "game-mechanics", "library", "magic", "management",
              "minigame", "mobs", "optimization", "storage", "technology", "transportation", "utility", "worldgen"]

ModSearchIndexes = ["relevance", "downloads", "follows", "newest", "updated"]

ModLoaderTypes = ["forge", "fabric"]


class SearchModInModrinth:
    def __init__(self, Keyword:str = None, index:str = None, Modfilter:str = None, ModLoaderType:str = None, ModMCVersion:str = None) -> None:
        """
            Modrinth资源搜索
            :param Keyword:搜索关键字
            :param index:排序方式(relevance:按匹配度排列
                                 downloads:按下载量排列
                                 follows:按浏览量排列
                                 newest:按Mod发布时间排列
                                 updated:按Mod最近更新时间排列)
            :param Modfilter:Mod类型
            :param ModLoaderType:Mod加载器类型
            :param ModMCVersion:指定搜索支持某个MC版本的mod
            
            Mod类别: ("adventure": 冒险
                     "cursed": 诅咒？
                     "decoration": 装饰
                     "equipment": 装备
                     "food": 食物
                     "game-mechanics": 游戏机制
                     "library": 支持库
                     "magic": 魔法
                     "management": 管理
                     "minigame": 小游戏
                     "mobs": 生物
                     "optimization": 优化
                     "social": 社交
                     "storage": 贮存
                     "technology": 科技
                     "transportation": 运输
                     "utility": 实用
                     "worldgen": 世界生成)
            Mod加载器类型: (forge, fabric)
        """
        self.Keyword = Keyword
        self.Index = index
        self.ModFilter = Modfilter
        self.ModLoaderType = ModLoaderType
        self.ModMCVersion = ModMCVersion
        
    def SearchMods(self) -> RequestResponse:
        """
            搜索
            :return: Type:请求api返回的response
        """
        RequestUrl = "https://mcim.z0z0r4.top/modrinth/search?"
        args = []
        if self.Keyword is not None:
            args.append(f"query={selfself.Keyword}")
        if self.Index is not None:
            args.append(f"index={self.Index}")
        if any([self.ModFilter, self.ModLoaderType, self.ModMCVersion]):
            facetslist = []
            if self.ModFilter is not None:
                facetslist.append([f"categories:{self.ModFilter}",])
            if self.ModLoaderType is not None:
                facetslist.append([f"categories:{self.ModLoaderType}",])
            if self.ModMCVersion is not None:
                facetslist.append([f"versions:{self.ModMCVersion}",])
            facetstr:str = str(facetslist)
            args.append(f"facets={facetstr}")
        RequestUrl += "&".join(args).replace('\'', '\"')
        return requests_get(RequestUrl);
    
