import requests
import json
import Accounts
from PyJsonEntity import PyJsonEntity

# YggdrasilAuthenticator 外置登录验证类
class YggdrasilAuthenticator:
    # authserver:外置登录提供商提供的api认证地址
    # mail:用户名(邮件)
    # password:密码
    def __init__(self, authserver:str, mail:str, password:str) -> None:
        self.mail = mail
        self.password = password
        self.authserver = authserver.strip("/")

    # 登录
    # return value:YggdrasilAccount类
    def Login(self):
        account = Accounts.YggdrasilAccount()
        RequestParams:dict = {
            "username": self.mail,
            "password": self.password,
            "agent":{
                "name": "Minecraft",
                "version": 1
            }
        }
        requesturl = self.authserver + "/authserver/authenticate"
        result = requests.post(requesturl, data=json.dumps(RequestParams, ensure_ascii=False),
                               headers={"Content-Type": "application/json"})
        if(result.status_code != 200):
            account.error = result.text
            return account
        else:
            return PyJsonEntity.JsonToEntity(result.text, account)
        
    # 刷新令牌
    # return value:YggdrasilAccount类
    def Refresh(self, account:Accounts.YggdrasilAccount):
        raccount = Accounts.YggdrasilAccount()
        RequestParams:dict = {
            "accessToken": account.accessToken
        }
        requesturl = self.authserver + "/authserver/refresh"
        result = requests.post(requesturl, data=json.dumps(RequestParams, ensure_ascii=False),
                               headers={"Content-Type": "application/json"})
        if(result.status_code != 200):
            raccount.error = result.text
            return raccount
        else:
            return PyJsonEntity.JsonToEntity(result.text, raccount)
        
    # 登出
    # return value:bool,是否成功
    def Signout(self) -> bool:
        RequestParams:dict = {
            "username": self.mail,
            "password": self.password
        }
        requesturl = self.authserver + "/authserver/signout"
        result = requests.post(requesturl, data=json.dumps(RequestParams, ensure_ascii=False),
                               headers={"Content-Type": "application/json"})
        if(result.status_code != 204):
            return False
        else:
            return True