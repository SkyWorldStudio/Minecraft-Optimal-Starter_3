# coding=utf-8
"""微软登陆(代码流)"""
import json
import time
import requests


class MicrosoftAuthenticator:
    def __init__(self, ClientId: str) -> None:
        """
            MicrosoftAuthenticator 微软登录类
            :param ClientId: 在Azure注册过的客户端ID
            :return: None
        """
        self.ClientId = ClientId
        self.Quit_ = False

    def StartDeviceFlowRequest(self):
        """
            应先执行这个方法，无参数，开启设备代码流验证
            :return (用于填写的UserCode, 进行验证的URL, 超时时间 单位:秒)
        """
        RequestParams: dict = {
            "client_id": self.ClientId,
            "scope": "XboxLive.signin offline_access"
        }
        res = requests.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode", data=RequestParams)
        returnContext: str = res.text
        if returnContext == "":
            return None
        returnJson = json.loads(returnContext)
        self.DeviceCode = returnJson["device_code"]
        self.Interval = returnJson["interval"]
        self.ExpiresIn = returnJson["expires_in"]
        return returnJson["user_code"], returnJson["verification_uri"], returnJson["expires_in"]

    def XBLAuthToken(self):
        """
            第三个执行，进行XBL验证
            :return: 验证结果
        """
        RequestParams: dict = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d=" + self.AccessToken
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)

        res = requests.post("https://user.auth.xboxlive.com/user/authenticate", data=RequestBody,
                            headers={"Content-Type": "application/json"})
        if res.text == "":
            return None

        context = json.loads(res.text)
        return context


    def XSTSAuthToken(self, XBLToken: str):
        """
            第四个验证,XSTS验证
            :param XBLToken: XBL验证结果中的Token
            :return: 验证结果
        """
        RequestParams: dict = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [XBLToken],
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)
        res = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", data=RequestBody,
                            headers={"Content-Type": "application/json"})
        if res.text == "":
            return None
        context = json.loads(res.text)
        return context


    def LoginWithXbox(self, XSTSAuthResponse: dict):
        """
            第五个验证，登录Xbox,
            :param XSTSAuthResponse: 进行XSTS验证获得的字典
            :return: 验证结果
        """
        RequestParams: dict = {
            "identityToken": "XBL3.0 x=%s;%s" % (
                XSTSAuthResponse["DisplayClaims"]["xui"][0]["uhs"], XSTSAuthResponse["Token"])
        }
        RequestBody = json.dumps(RequestParams, ensure_ascii=False)
        res = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", data=RequestBody,
                            headers={"Content-Type": "application/json"})
        if res.text == "":
            return None
        context = json.loads(res.text)
        return context


    def isTheAccountHasMinecraft(self, AuthToken: str) -> bool:
        """
            用于验证账号是否有正版mc
            :param AuthToken: 登录Xbox获得的AccessToken
            :return: True or False
        """
        headers = {"Authorization": "Bearer " + AuthToken}
        res = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers=headers)
        if res.text == "":
            return False
        context = json.loads(res.text)
        if "error" in dict(context).keys():
            return False
        else:
            for i in context["items"]:
                if i["name"] == "game_minecraft":
                    return True
        return False


    def GetPlayerProfile(self, AuthToken: str):
        """
            用于获取玩家信息
            :param AuthToken: 登录Xbox获得的AccessToken
            :return: 验证结果
        """
        headers = {"Authorization": "Bearer " + AuthToken}
        res = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers)
        if res.text == "":
            return None
        context = json.loads(res.text)
        return context

    def WaitForUserCompletedAuth(self):
        """
            第二个调用，等待用户完成验证
            :return: True or False
        """
        while True:
            if self.Quit_:
                break
            else:
                time.sleep(self.Interval)
                RequestParams: dict = {
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "client_id": self.ClientId,
                    "device_code": self.DeviceCode
                }
                result = requests.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                                       data=RequestParams)
                if result.text == "":
                    return None
                returnJson = json.loads(result.text)
                if result.status_code >= 200 and result.status_code < 300:
                    self.AccessToken = returnJson["access_token"]
                    self.RefreshToken = returnJson["refresh_token"]
                    return True
                else:
                    if returnJson["error"] != "authorization_pending":
                        return False


    def Quit(self):
        self.Quit_ = True

    def StartRefreshToken(self) -> list:
        """
            刷新令牌,进行设备代码流成功后可以调用
            :return [True,AccessToken,RefreshToken] or [False]
        """
        RequestParams:dict = {
            "grant_type": "refresh_token",
            "client_id": self.ClientId,
            "refresh_token": self.RefreshToken
        }
        result = requests.post("https://login.live.com/oauth20_token.srf", data=RequestParams)
        if result.text == "":
            return [False]
        resjson = json.loads(result.text)
        self.AccessToken = resjson["access_token"]
        self.RefreshToken = resjson["refresh_token"]
        return [True,self.AccessToken,self.RefreshToken]



if __name__ == "__main__":
    arg1 = MicrosoftAuthenticator('35402e6c-8e66-4bf2-8f9b-a1de642db842')
    arg2 = arg1.StartDeviceFlowRequest()
    print(arg2)
    arg3 = arg1.WaitForUserCompletedAuth()
    print('等待验证：' + str(arg3))
    arg4 = arg1.XBLAuthToken()
    print('验证结果' + str(arg4))
    arg5 = arg1.XSTSAuthToken(arg4["Token"])
    print('验证结果' + str(arg5))
    arg6 = arg1.LoginWithXbox(arg5)
    print('验证结果' + str(arg6))
    arg7 = arg1.isTheAccountHasMinecraft(arg6["access_token"])
    print('账号是否有正版mc' + str(arg7))
    arg8 = arg1.GetPlayerProfile(arg6["access_token"])
    print('验证结果' + str(arg8))
    access_token = arg6['access_token']

