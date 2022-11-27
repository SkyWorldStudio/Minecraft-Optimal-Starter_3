"""异步下载大文件"""

import asyncio
import aiohttp
import datetime
import os
from sys import platform
import requests
import time
from gevent import monkey
import gevent



class Download:
    def __init__(self) -> None:
        super(Download, self).__init__()

    def download(self, url, path, parh_cache):
        self.parh_cache = parh_cache
        self.url = url
        self.path = path
        # 先检查文件大小
        headers={
            "Accept-Encoding": "identity",
            'session':'JSESSIONID',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        r=requests.get(url,stream=True,headers=headers)
        file_size_str_=r.headers['Content-Length'] #提取出来的是个数字str
        self.file_size_str = int(file_size_str_)
        self.file_size_str_MB = int(file_size_str_)//1024/1024
        print(self.file_size_str_MB)
        print(self.file_size_str)

        if self.file_size_str_MB >= 0.2:
            # 如果大于0.2MB 就分段异步下载
             
            self.new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.new_loop)
            asyncio.run(self.Download_Subsection_Start_Start())
        else:
            r = requests.get(url,stream=False)
            with open(path, 'wb') as fb:
                fb.write(r.content)
               
    async def Download_Subsection_Start_Start(self):
        # 启动用来批量启动协程的协程
        t = time.time()  # 获取时间
        print(t)
        self.parh_cache_ = os.path.join(self.parh_cache,str(t))  # 缓存路径
        file_size_str_l = 0
        file_size_str_l_to = 0
        Download_Number = -1
        # self.Download_Subsection = {}
        self.Download_Subsection_ = []
        self.Download_Subsection__ = []
        while True:
            # file_size_str_l 和 file_size_str_l_to：从…下载到……
            if file_size_str_l < self.file_size_str:
                Download_Number += 1  # 次数加一(用于拼接缓存目录)
                if Download_Number == 0:
                    # 如果是第一次 那么就将开始值设为0
                    file_size_str_l = 0
                else:
                    file_size_str_l = int(file_size_str_l_to)
                file_size_str_l_to = file_size_str_l+ 5242880
                if file_size_str_l_to < self.file_size_str:
                    pass
                else:
                    # 如果超过了文件大小 就改成最大
                    file_size_str_l_to = self.file_size_str
                file = os.path.join(self.parh_cache_,str(Download_Number) + '.MOS_Download')
                if file_size_str_l == file_size_str_l_to:
                    pass
                else:
                    a = {
                        'Download_Number': Download_Number,  # 下载次数
                        'size_star': file_size_str_l,  # 从……开始
                        'size_to': file_size_str_l_to, # 下载到……
                        'file': file  # 缓存到……
                    }
                    
                    self.Download_Subsection_.append(
                        asyncio.ensure_future(self.Download_Subsection(a))
                        )
            else:
                print(self.Download_Subsection)
                break
        await asyncio.wait([self.Download_Subsection_Start(self.Download_Subsection_)])
    
    async def Download_Subsection_Start(self, Download_Subsection):
        await asyncio.wait(Download_Subsection)
        # 检查是否完全完成
        if len(Download_Subsection) != 0:
            print('没有全部完成')
        else:
            print('ooooookkk')
    
    async def Download_Subsection(self,Download_Subsection):
        print(Download_Subsection)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        headers['Range'] = 'bytes=' + str(Download_Subsection['size_star']) + '-' + str(Download_Subsection['size_to'])
        print(headers)
        # 重试5次
        try:
            async with aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(connect=30)) as session:
                f = await session.get(self.url, headers=headers, ssl=False)
                f_code = await f.read()
                os.makedirs(self.parh_cache_,exist_ok=True)
                with open(Download_Subsection['file'], 'wb') as f:
                    f.write(f_code)
                #self.Download_Subsection__ = []

                self.Download_Subsection_[Download_Subsection['Download_Number']] = None
                print(self.Download_Subsection_)

        except aiohttp.client_exceptions.ClientConnectorError:
            print('客户端链接错误')
            if 'C' in Download_Subsection:
                Download_Subsection['C'] += 1
            else:
                Download_Subsection['C'] = 1

        print('OK')

    def DownloadAll(self, url_list, path_list):
        """
        first arg:
            url_list is a list,include the url of file you want to download
        second arg:
            path_list is a list,include the path of file you want to download
        """
        j = 0
        li = []
        for i in url_list:
            li.append(gevent.spawn(Download.download, i, path_list[j]))
            j += 1
        gevent.joinall(li)

if __name__ == '__main__':
    U = 'https://download-ssl.firefox.com.cn/releases/firefox/107.0/zh-CN/Firefox-latest.dmg'
    F = '/Users/xyj/Documents/临时/Firefox-latest.dmg'
    P_F = '/Users/xyj/Documents/临时/Firefox-latest__'
    a = Download()
    a.download(U,F,P_F)