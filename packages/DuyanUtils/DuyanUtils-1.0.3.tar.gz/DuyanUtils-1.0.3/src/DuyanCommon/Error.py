class Error(Exception):
    def __init__(self, code, message):
        super().__init__(f"{message}[CODE:{code}]")


class TimeError(Error):
    """
        时间类的错误 code 10300 - 10399
    """
    pass


class TimeNoFormatError(TimeError):
    def __init__(self):
        """
            时间格式确实
        """
        super().__init__(code=10300, message="时间格式缺失")


class TimeConversionTypeError(TimeError):
    def __init__(self):
        """ 时间转换格式不正确"""
        super().__init__(code=10301, message="转换时间类型不是标准的时间类型")


class ConversionTypeError(Error):
    def __init__(self, message=None):
        super().__init__(code=10001, message=message and "类型错误:{}".format(message) or "目标类型错误")


class NullPointError(Error):
    def __init__(self):
        """ 空指针通用类型 """
        super().__init__(code=10000, message="空指针")


class ParamError(Error):
    def __init__(self):
        super().__init__(code=10002, message="入参不正确")


class PageError(Error):
    def __init__(self):
        super().__init__(code=10003, message="页码不能为空或小于0")


class SizeError(Error):
    def __init__(self):
        super().__init__(code=10004, message="分页展示数量不能小于0")


class OverSizeLimitError(Error):
    def __init__(self):
        super().__init__(code=10005, message="分页展示数量超过限制")


class VersionLowError(Error):
    def __init__(self, name, version):
        super().__init__(code=10006, message=f"当前{name}版本过低，请使用制定版本[{version}]")


class SQLFormatError(Error):
    def __init__(self, sql):
        super().__init__(code=10101, message=f"当前sql有误[{sql}]")


class SQLNotInsertError(Error):
    def __init__(self, sql):
        super().__init__(code=10102, message=f"当前sql不是INSERT语句[{sql}]")


class SQLNotUpdateError(Error):
    def __init__(self, sql):
        super().__init__(code=10103, message=f"当前sql不是UPDATE语句[{sql}]")


class SQLNotDeleteError(Error):
    def __init__(self, sql):
        super().__init__(code=10104, message=f"当前sql不是DELETE语句[{sql}]")


class SQLNotSelectError(Error):
    def __init__(self, sql):
        super().__init__(code=10105, message=f"当前sql不是DELETE语句[{sql}]")
