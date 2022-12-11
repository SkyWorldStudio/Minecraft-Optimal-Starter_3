# coding=utf-8
import json

import requests
import os
from Code.Code import JsonWrite,print_

class GamePublishListReturn:
    def __init__(self,Source,File) -> None:
        """
            请求游戏版本列表
            :param Source: 下载源(MC: MC官方 / MCBBS: MCBBS源 / BMCLAPI: BMCLAPI源)
            :param File: 缓存目录
        """
        super(GamePublishListReturn, self).__init__()
        self.Source = Source
        self.File = File
        
    def ListReturn(self,Kind):
        """
            请求原版列表
            :param Kind: 种类(release: 原版 / snapshot: 快照版/ old_alpha: 远古版本)
            :return: 游戏列表(List)
        """
        if self.Source == 'MC':
            URL = 'https://launchermeta.mojang.com/mc/game/version_manifest_v2.json'
        elif self.Source == 'MCBBS':
            URL = 'https://download.mcbbs.net/mc/game/version_manifest_v2.json'
        else:
            URL = 'https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json'

        headers = {
                'User-Agent': 'Mozilla/55.0 (Macintosh; Intel Mac OS X 55.55; rv:101.0) Gecko/20100101 Firefox/101.0'
                }
        r = requests.get(URL, headers=headers)
        J = r.json()['versions']
        File_ = os.path.join(self.File,'Versions')
        os.makedirs(File_, exist_ok=True)
        File = os.path.join(File_,'Versions.json')
        JsonWrite(r.json(),File,BuBug=True)
        L = []
        for J_1 in J:
            # print_('BeBug',J_1)
            if J_1['type'] == Kind:
                L.append(J_1)
        # print_('BeBug',L)
        return L

        # 释放缓存
        # r.close()

if __name__ == '__main__':
    a = GamePublishListReturn('MC','/Users/xyj/Documents/.MOS')
    a.ListReturn('MCBBS')
        
        
        
        