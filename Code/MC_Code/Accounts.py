class Account:
    def __init__(self) -> None:
        self.name = None
        self.uuid = None
        self.accessToken = None
        self.refresh_token = None
        self.error = None

class OfflineAccount(Account):
    pass

# Microsoft类 --Begin--
class MicrosoftAccount:
    def __init__(self) -> None:
        super().__init__()
        self.name = None
        self.id = None
        self.access_token = None
        self.refresh_token = None
        self.skins = [MicrosoftPlayerSkin()]
        self.error = None

class MicrosoftPlayerSkin:
    def __init__(self) -> None:
        self.id = None
        self.state = None
        self.url = None
        self.variant = None
        self.alias = None

# Microsoft类 --End--

# Yggdrasil类 --Begin--
class YggdrasilAccount:
    def __init__(self) -> None:
        super().__init__()
        self.name = None
        self.uuid = None
        self.accessToken = None
        self.availableProfiles = [YggdrasilProfile()]
        self.selectedProfile = YggdrasilProfile()
        self.error = None
        
class YggdrasilProfile():
    def __init__(self) -> None:
        self.id = None
        self.name = None

# Yggdrasil类 --End--