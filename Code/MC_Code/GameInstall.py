# coding=utf-8
import asyncio
import json
import os
import random
import time
import traceback

import aiohttp
import requests
import queue

from Code.Code import Sha1, Hash


class GameInstall():
    def __init__(self, GameFile_M, GameFile_V, File, Download_Source, V_JsonFile,
                 V, Name, V_Forge,V_Fabric,V_Optifine,
                 Systeam,Systeam_V,
                 Sha1Cleck,MaxConcurrence):
        """
            游戏安装
            :param GameFile_M: 游戏根目录(.minecraft目录)
            :param GameFile_V: 游戏目录
            :param File: MOS缓存目录
            :param Download_Source: 下载源(MCBBS, BMCLAPI, MC)
            :param V_JsonFile: 游戏Json目录(版本列表的)
            :param V: MC版本
            :param Name: 游戏名
            :param V_Forge: Forge版本
            :param V_Fabric: Fabric版本
            :param V_Optifine: Optifine版本
            :param Systeam: 系统种类(Windows, Mac, Linux)
            :param Systeam_V: 系统版本(10,14.4.1)
            :param Sha1Cleck: 是否进行Sha1检查
            :param MaxConcurrence: 最大并发数
        """
        self.GameFile_M = GameFile_M
        self.GameFile_V = GameFile_V
        self.File = File
        self.Download_Source = Download_Source
        self.V_JsonFile = V_JsonFile
        self.V = V
        self.Name = Name
        self.V_Forge = V_Forge
        self.V_Fabric = V_Fabric
        self.V_Optifine = V_Optifine
        self.Systeam = Systeam
        self.Systeam_V = Systeam_V
        self.Sha1Cleck = Sha1Cleck
        self.MaxConcurrence = MaxConcurrence

        if self.Download_Source == 'MC':
            # self.Download_Source_Url_Json_Q = 'http://launchermeta.mojang.com/'
            self.Download_Source_Url_Libraries_Q = 'http://libraries.minecraft.net/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://resources.download.minecraft.net/'  # 资源文件
        elif self.Download_Source == 'MCBBS':
            self.Download_Source_Url_Json_Q = 'http://download.mcbbs.net/'  # json文件
            self.Download_Source_Url_Libraries_Q = 'http://download.mcbbs.net/maven/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://download.mcbbs.net/assets/'  # 资源文件
        else:
            self.Download_Source_Url_Json_Q = 'http://bmclapi2.bangbang93.com/'  # json文件
            self.Download_Source_Url_Libraries_Q = 'http://bmclapi2.bangbang93.com/maven/'  # 依赖
            self.Download_Source_Url_Resources_Q = 'http://bmclapi2.bangbang93.com/assets/'  # 资源文件


        super(GameInstall, self).__init__()

    def Run(self):
        # 下载MC Json文件
        # 拼接路径
        if self.Download_Source == 'MC':
            with open(self.V_JsonFile, 'r', encoding='utf_8') as f:
                b = json.load(f)
            for b_1 in b['versions']:
                if b_1['id'] == self.MC:
                    url = b_1['url']
                    break
        else:
            url = self.Download_Source_Url_Json_Q + 'version/' + self.V + '/json'

        # 下载
        V_Json_Get = requests.get(url)
        V_Json = V_Json_Get.json()
        V_Json['id'] = self.Name
        os.makedirs(self.GameFile_V, exist_ok=True)
        V_Json_File = os.path.join(self.GameFile_V,str(self.Name + '.json'))
        with open(V_Json_File, 'w+', encoding='utf-8') as f:
            json.dump(V_Json, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

        # 下载Assets List Json文件
        AssetsList_Json = V_Json['assetIndex']
        try:
            url = self.Download_Source_Url_Json_Q + AssetsList_Json['url'].split('https://piston-meta.mojang.com/')[1]
        except IndexError:
            url = self.Download_Source_Url_Json_Q + AssetsList_Json['url'].split('https://launchermeta.mojang.com/')[1]
        id = AssetsList_Json['id']
        path_up = os.path.join(self.GameFile_M, 'assets', 'indexes')
        path = os.path.join(path_up, id + '.json')
        AssetsList_Json_Get = requests.get(url)
        AssetsList_Json = AssetsList_Json_Get.json()
        os.makedirs(path_up, exist_ok=True)
        with open(path, 'w+', encoding='utf-8') as f:
            json.dump(AssetsList_Json, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

        MainJar = {}
        self.Libraries = []
        self.Assets = []

        # Jar文件解析
        MainJar['url'] = V_Json['downloads']['client']['url']
        MainJar['size'] = V_Json['downloads']['client']['size']
        MainJar['sha1'] = V_Json['downloads']['client']['sha1']

        import re
        # Libraries文件解析
        for L in V_Json['libraries']:
            if 'rules' in L:
                for R in L['rules']:
                    if len(R) != 1:
                        if R['action'] == 'disallow':
                            # 如果写的是禁止
                            R.pop('action')
                            for a in R:
                                if R[a]['name'] == 'osx':
                                    if self.Systeam == 'Mac':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m == None:
                                            # 如果不在限制以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries',A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        print('l_on')
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-osx']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-osx']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

                                elif R[a]['name'] == 'windows':
                                    if self.Systeam == 'Win':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m == None:
                                            # 如果不在限制以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-windows']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-windows']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

                                elif R[a]['name'] == 'linux':
                                    if self.Systeam == 'Linux':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m == None:
                                            # 如果不在限制以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-linux']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-linux']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

                        elif R['action'] == 'allow':
                            # 如果写的是允许
                            R.pop('action')
                            for a in R:
                                if R[a]['name'] == 'osx':
                                    if self.Systeam == 'Mac':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m != None:
                                            # 如果在允许以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-osx']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-osx']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

                                elif R[a]['name'] == 'windows':
                                    if self.Systeam == 'Win':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m != None:
                                            # 如果在允许以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-windows']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-windows']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

                                elif R[a]['name'] == 'linux':
                                    if self.Systeam == 'Linux':
                                        # 如果系统匹配就进行正则表达式判断
                                        if 'version' in R[a]:
                                            # 如果写了系统版本限制规则
                                            r = R[a]['version']
                                            m = re.search(r, self.Systeam_V)
                                        else:
                                            m = ''  # 让下面的if, 识别为"允许"
                                        Sh = A['sha1']
                                        if m != None:
                                            # 如果在允许以内,就添加
                                            URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                                            Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                                            Path_Up = os.path.abspath(os.path.join(Path, ".."))
                                            if os.path.exists(Path):
                                                # 如果目录存在
                                                if self.Sha1Cleck:
                                                    s = Sha1(Path)
                                                    if s != Sh:
                                                        if 'artifact' in L['downloads']:
                                                            A = L['downloads']['artifact']
                                                            Zip = False
                                                        else:
                                                            A = L['downloads']['classifiers']['natives-linux']
                                                            Zip = True
                                                        self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                                            else:
                                                if 'artifact' in L['downloads']:
                                                    A = L['downloads']['artifact']
                                                    Zip = False
                                                else:
                                                    A = L['downloads']['classifiers']['natives-linux']
                                                    Zip = True
                                                self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

            else:
                # 没有规则限制
                if self.Systeam == 'Mac':
                    if 'artifact' in L['downloads']:
                        A = L['downloads']['artifact']
                        Zip = False
                    else:
                        A = L['downloads']['classifiers']['natives-osx']
                        Zip = True
                elif self.Systeam == 'Win':
                    if 'artifact' in L['downloads']:
                        A = L['downloads']['artifact']
                        Zip = False
                    else:
                        A = L['downloads']['classifiers']['natives-windows']
                        Zip = True
                elif self.Systeam == 'Linux':
                    if 'artifact' in L['downloads']:
                        A = L['downloads']['artifact']
                        Zip = False
                    else:
                        A = L['downloads']['classifiers']['natives-linux']
                        Zip = True
                URL = self.Download_Source_Url_Libraries_Q + A['url'].split('https://libraries.minecraft.net/')[1]
                Path = os.path.join(self.GameFile_M, 'libraries', A['path'])
                Path_Up = os.path.abspath(os.path.join(Path, ".."))
                Sh = A['sha1']
                if os.path.exists(Path):
                    # 如果目录存在
                    if self.Sha1Cleck:
                        s = Sha1(Path)
                        if s != Sh:
                            if 'artifact' in L['downloads']:
                                A = L['downloads']['artifact']
                                Zip = False
                            else:
                                A = L['downloads']['classifiers']['natives-linux']
                                Zip = True
                            self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])
                else:
                    self.Libraries.append(['Libraries',URL, Path_Up, Path, A['size'], Sh, Zip])

        # Assets文件解析
        for A in AssetsList_Json['objects']:
            # 注意, MC官方这里写的hash其实是sha1算法
            hash = AssetsList_Json['objects'][A]['hash']
            url = self.Download_Source_Url_Resources_Q + hash[0:2] + '/' +hash
            size = AssetsList_Json['objects'][A]['size']
            path_up = os.path.join(self.GameFile_M,'assets','objects',hash[0:2])
            path = os.path.join(path_up,hash)
            if os.path.exists(path):
                # 如果文件存在就判断hash值
                h = Sha1(path)
                if h != hash:
                    print('no')
                    self.Assets.append(['Assets',url, path_up, path, hash, size])
            else:
                self.Assets.append(['Assets',url, path_up, path, hash, size])

        print(MainJar)
        print('================')
        #print(self.Libraries)
        print(len(self.Libraries))
        print('================')
        #print(Assets)
        print(len(self.Assets))

        print('准备下载')
        self.AllList = self.Libraries + self.Assets
        self.I = len(self.AllList) + 1
        print('一共' + str(self.I) + '项文件')

        import time
        # 创建
        time_start = time.perf_counter()
        print('开始下载')
        while True:
            if len(self.AllList) !=0:
                if len(self.AllList) <= len(self.Assets):
                    i = 60
                else:
                    i = 30
                self.new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.new_loop)
                asyncio.run(self.DownloadTaskMake(i))
            else:
                break

        print('下载完成')
        time_stop = time.perf_counter()
        time = (time_stop-time_start)
        print('用时' + str(time))


    async def DownloadTaskMake(self,i):
        b = []
        for a in self.AllList[0:i]:
            # b.append(asyncio.ensure_future(self.Download(a)))
            b.append(self.Download(a))
        await asyncio.wait(b)



    #async def DownloadTask(self, queue,list):
    #    while True:
    #        try:
    #            print('取出')
    #            # 从队列中取出任务
    #            task = await queue.get()
    #            # 处理任务
    #            # await self.Download(task)
    #            await asyncio.wait([self.Download(task)])
    #            if task not in self.AllList:
    #                # 通知队列任务已被处理完成
    #                queue.task_done()
    #        except:
    #            traceback.print_exc()



    async def Download(self,list):
        """异步任务"""
        print('任务运行')
        print(list)
        headers = {}
        url = list[1]
        path_up = list[2]
        path = list[3]
        os.makedirs(path_up, exist_ok=True)
        #a = random.sample(range(1, 2), 1)
        #if a == 1:
        #    # 50%的概率进行等待
        #    a = random.sample(range(1, 10), 1)
        #    await asyncio.sleep(a/100)
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(connect=20)) as session:
                f = await session.get(url, headers=headers, ssl=False)
                f_code = await f.read()
                with open(path, 'wb') as f:
                    f.write(f_code)
                # f_code = ''  # 释放缓存
                self.AllList.remove(list)
                print(str(len(self.AllList)) + 'ok')
                #break
        except aiohttp.client_exceptions.ServerTimeoutError:
            pass
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass
        except aiohttp.client_exceptions.ClientConnectorError:
            pass
        except aiohttp.client_exceptions.ClientOSError:
            pass
        except:
            traceback.print_exc()
            print("出现异常")
            #break








if __name__ == '__main__':
    #a = GameInstall('/Users/xyj/Documents/.minecraft','/Users/xyj/Documents/.minecraft/versions/1.18.1/','/Users/xyj/Documents/.MOS','MCBBS','/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #      '1.18.1','1.18.1',None,None,None,'Mac','11.6.5',True)
    #a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/a1.0.11/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                'a1.0.11', 'a1.0.11', None, None, None,'Mac','11.6.5',True,0)
    a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.12.2/',
                    '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
                    '1.12.2', '1.12.2', None, None, None,'Mac','11.6.5',True,0)
    #a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.16.1/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                '1.16.1', '1.16.1', None, None, None, 'Mac', '11.6.5', True, 0)
    #a = GameInstall('/Users/xyj/Documents/.minecraft', '/Users/xyj/Documents/.minecraft/versions/1.9.1/',
    #                '/Users/xyj/Documents/.MOS', 'MCBBS', '/Users/xyj/Documents/.MOS/Versions/Versions.json',
    #                '1.9.1', '1.9.1', None, None, None,'Mac','11.6.5',True)
    a.Run()