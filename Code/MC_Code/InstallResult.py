class InstallResult:
    def __init__(self, isSuccess:bool, ErrorMessage:str = None, OtherArgs = None) -> None:
        self.isSuccess = isSuccess
        self.ErrorMessage = ErrorMessage
        self.OtherArgs = OtherArgs