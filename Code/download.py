import os
from sys import platform
import requests
import time
from gevent import monkey
import gevent
class Download:
    def __init__(self) -> None:
        pass
    def download(url,path):
        r=requests.get(url)
        with open(path,'wb') as fb:
            fb.write(r.content)
    def download_all(self,url_list,path_list):
        '''
        first arg:
            url_list is a list,include the url of file you want to download
        second arg:
            path_list is a list,include the path of file you want to download
        '''
        j=0
        li=[]
        for i in url_list:
            li.append(gevent.spawn(Download.download,i,path_list[j]))
            j+=1
        gevent.joinall(li)