import requests
import json
import time


# MicrosoftAuthenticator 微软登录类
# param ClientId:在Azure注册过的客户端ID
class MicrosoftAuthenticator:
    def __init__(self, ClientId:str) -> None:
        self.ClientId = ClientId
    

    #应先执行这个方法，无参数，开启设备代码流验证
    #返回值:元组
    #[0]用于填写的UserCode,[1]进行验证的URL,[2]超时时间，单位秒
    def StartDeviceFlowRequest(self) -> tuple:
        RequestParams:dict = {
            "client_id":self.ClientId,
            "scope": "XboxLive.signin offline_access"
        }
        res = requests.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode", data=RequestParams)
        returncontext:str = res.text;
        if(returncontext == ""):return None
        returnjson = json.loads(returncontext)
        self.DeviceCode = returnjson["device_code"]
        self.Interval = returnjson["interval"]
        self.ExpiresIn = returnjson["expires_in"]
        return (returnjson["user_code"], returnjson["verification_uri"], returnjson["expires_in"])
    
    #第三个执行，进行XBL验证
    #返回值:验证结果
    def XBLAuthToken(self) -> dict:
        RequestParams:dict = {
            "Properties":{
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d=" + self.AccessToken
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)
        res = requests.post("https://user.auth.xboxlive.com/user/authenticate", data=RequestBody, headers={"Content-Type": "application/json"})
        if(res.text == ""):return None
        context = json.loads(res.text)
        return context
    
    #第四个验证,XSTS验证,XBLToken:XBL验证结果中的Token
    #返回值:验证结果
    def XSTSAuthToken(self, XBLToken:str) -> dict:
        RequestParams:dict = {
            "Properties":{
                "SandboxId": "RETAIL",
                "UserTokens": [XBLToken],
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)
        res = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", data=RequestBody, headers={"Content-Type": "application/json"})
        if(res.text == ""):return None
        context = json.loads(res.text)
        return context

    #第五个验证，登录Xbox,XSTSAuthResponse:进行XSTS验证获得的字典
    #返回值:验证结果
    def LoginWithXbox(self, XSTSAuthResponse:dict) -> dict:
        RequestParams:dict = {
            "identityToken": "XBL3.0 x=%s;%s" % (XSTSAuthResponse["DisplayClaims"]["xui"][0]["uhs"], XSTSAuthResponse["Token"]                                                                                                      )
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)
        res = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", data=RequestBody, headers={"Content-Type": "application/json"})
        if(res.text == ""):return None
        context = json.loads(res.text)
        return context
    
    #用于验证账号是否有正版mc,AuthToken:登录Xbox获得的AccessToken
    #返回值:布尔值
    def isTheAccountHasMinecraft(self, AuthToken:str) -> bool:
        headers = {"Authorization":"Bearer " + AuthToken}
        res = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers=headers)
        if(res.text == ""):return False
        context = json.loads(res.text)
        if("error" in dict(context).keys()):return False
        else:
            for i in context["items"]:
                if(i["name"] == "game_minecraft"):return True
        return False
    
    #用于获取玩家信息,AuthToken:登录Xbox获得的AccessToken
    #返回值:验证结果
    def GetPlayerProfile(self, AuthToken:str) -> dict:
        headers = {"Authorization":"Bearer " + AuthToken}
        res = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers)
        if(res.text == ""):return None
        context = json.loads(res.text)
        return context
    

    #第二个调用，等待用户完成验证
    #返回值:布尔值，验证是否成功
    def WaitForUserCompletedAuth(self) -> bool:
        while True:
            time.sleep(self.Interval)
            RequestParams:dict = {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": self.ClientId,
                "device_code": self.DeviceCode
            }
            result = requests.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token", data=RequestParams)
            if(result.text == ""):return None
            resjson = json.loads(result.text)
            if(result.status_code >= 200 and result.status_code < 300):
                self.AccessToken = resjson["access_token"]
                self.RefreshToken = resjson["refresh_token"]
                return True
            else:
                if(resjson["error"] != "authorization_pending"):return False

    #刷新令牌,进行设备代码流成功后可以调用
    def StartRefreshToken(self) -> bool:
        RequestParams:dict = {
            "grant_type": "refresh_token",
            "client_id": self.ClientId,
            "refresh_token": self.RefreshToken
        }
        result = requests.post("https://login.live.com/oauth20_token.srf", data=RequestParams)
        if(result.text == ""):return False
        resjson = json.loads(result.text)
        self.AccessToken = resjson["access_token"]
        self.RefreshToken = resjson["refresh_token"]
        return True

