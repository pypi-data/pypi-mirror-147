# -*- coding: UTF-8 -*-
import json
import random
import re
import time
from datetime import datetime, date, timedelta
from typing import Tuple

from Error import TimeNoFormatError, ConversionTypeError, NullPointError, TimeConversionTypeError, ParamError


class Entity(object):
    def __init__(self, data: dict = None):
        if data is None:
            return
        for key in data:
            value = data.get(key)
            self.__setattr__(str(key), value)

    def __str__(self):
        var = dict()
        for key in self.__dir__():
            if key.startswith("__") or "build_list" == key:
                continue
            var[key] = self.__getattribute__(key)
        return str(var)

    @staticmethod
    def build_list(data_list: list[dict]):
        res = list()
        if data_list is None or len(data_list) == 0:
            return res
        for item in data_list:
            if isinstance(item, Entity):
                res.append(item)
            else:
                res.append(Entity(item))
        return res


class EntityPage(object):
    def __init__(self):
        self.page = None
        self.size = None
        self.total = None
        self.page_size = None
        self.data = None

    def __str__(self):
        var = dict()
        for key in self.__dir__():
            if key.startswith("__") or "build_obj" == key :
                continue
            if "data" == key:
                data = self.__getattribute__(key)
                var[key] = [str(i) for i in data]
            else:
                var[key] = self.__getattribute__(key)
        return str(var)

    @staticmethod
    def build_obj(data, page: int = None, size: int = None, total: int = None):
        entity = EntityPage()
        entity.data = Entity.build_list(data)
        entity.page = page
        entity.size = size
        entity.total = total
        entity.page_size = entity.data and len(entity.data) or 0
        return entity


class Utils(object):
    """
        通用工具
    """
    NUMERICAL_REGX = r"^\d+$"  # 数字类型正则
    EMAIL_REGX = r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
    MOBILE_REGX = r"^(\+86){0,1}0{0,1}1[3-9]\d{9}$"

    @staticmethod
    def get_random_int(start: int = 0, end: int = 9) -> int:
        """
            获取指定范围的随机数
        :param start:
        :param end:
        :return:
        """
        return random.randint(start, end)

    @staticmethod
    def get_random_len(_len: int = 1) -> str:
        if _len <= 0:
            raise ParamError
        x = pow(10, _len) - 1
        var = str(Utils.get_random_int(0, x))
        while len(var) < _len:
            var = "0" + var
        return var

    @staticmethod
    def is_empty(var):
        """
            判空
        :param var:
        :return:
        """
        if var is None or len(str(var)) == 0:
            return True
        if isinstance(var, str):
            return len(var.strip()) == 0
        if isinstance(var, list) or isinstance(var, dict) or isinstance(var, Tuple):
            return len(var) == 0
        return False

    @staticmethod
    def is_numerical(var: str):
        """
            判断是否是数字
        :param var:
        :return:
        """
        if Utils.is_empty(var):
            return False
        r = re.search(Utils.NUMERICAL_REGX, var)
        return r is not None

    @staticmethod
    def get_numerical(var: str):
        """
            拿数字
        :param var:
        :return:
        """
        if var is None:
            raise NullPointError()
        if not Utils.is_numerical(var):
            raise ConversionTypeError(f"{var}不是整型")
        return int(var)

    @staticmethod
    def is_email(var: str):
        """
            判断是否是email
        :param var:
        :return:
        """
        if Utils.is_empty(var):
            return False
        r = re.search(Utils.EMAIL_REGX, var)
        return len(r.group()) > 0 if r else False

    @staticmethod
    def is_mobile(var: str):
        """
            判断是否是手机号
        :param var:
        :return:
        """
        if Utils.is_empty(var):
            return False
        r = re.search(Utils.MOBILE_REGX, var)
        return len(r.group()) > 0 if r else False


class TimeUtils(object):
    """
        时间 工具
    """
    DATETIME_FORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_MILLISECOND = "%Y-%m-%d %H:%M:%S.%f"
    DATE_FORMAT_DEFAULT = "%Y-%m-%d"

    @staticmethod
    def is_out_day(var: datetime, year=0, month=0, day=0, hour=0, minute=0, second=0):
        """
            判断时间是否超过了制定日期范围
        :param var: 制定时间
        :param year: 年限
        :param month: 月数
        :param day: 天数
        :param hour: 小时数
        :param minute: 分钟数
        :param second: 秒数
        :return:
        """
        now = datetime.now()
        #  当前时间比 参数大的时候，判断下限
        if now.__gt__(var):
            limit_day = datetime(year=now.year - year if year > 0 else now.year,
                                 month=now.month - month if month > 0 else now.month,
                                 day=now.day - day if day > 0 else now.day,
                                 hour=now.hour - hour if hour > 0 else now.hour,
                                 minute=now.minute - minute if minute > 0 else now.minute,
                                 second=now.second - second if second > 0 else now.second)
            return limit_day.__gt__(var)
        else:
            # 当前时间比参数小的时候 ，判断上限
            limit_day = datetime(year=now.year + year if year > 0 else now.year,
                                 month=now.month + month if month > 0 else now.month,
                                 day=now.day + day if day > 0 else now.day,
                                 hour=now.hour + hour if hour > 0 else now.hour,
                                 minute=now.minute + minute if minute > 0 else now.minute,
                                 second=now.second + second if second > 0 else now.second)
            return limit_day.__lt__(var)

    @staticmethod
    def get_now_str(_format: str):
        """
            获取当前时间的格式化字符串
        :param _format:
        :return:
        """
        return datetime.now().strftime(_format)

    @staticmethod
    def end_day_surplus_second(var: datetime = None):
        """
            获取指定时间当天的剩余时间
        :param var:  None able ，default now
        :return:
        """
        if var is None:
            var = datetime.now()
        end_of_day = TimeUtils.get_end_of_day(var)
        return TimeUtils.get_datetime_diff(var, end_of_day)

    @staticmethod
    def is_in_month(var1: datetime, var2: datetime):
        """
            判断同一个月 跨月按30天算 ，不跨越按自然月算
        :param var1:
        :param var2:
        :return:
        """
        in_same_month = TimeUtils.is_in_same_month(var1, var2)
        if in_same_month:
            return True
        diff = TimeUtils.get_datetime_diff_day(var1, var2)
        return abs(diff) <= 30

    @staticmethod
    def is_in_same_month(var1: datetime, var2: datetime):
        """
            判断同一个月 月份相同
        :param var1:
        :param var2:
        :return:
        """
        return var1.year == var2.year and var1.month == var2.month

    @staticmethod
    def is_in_day(var1: datetime, var2: datetime):
        """
            是否是一天内 ，判断的是秒数
        :param var1:
        :param var2:
        :return:
        """
        diff_seconds = TimeUtils.get_datetime_diff(var1, var2)
        return abs(diff_seconds) <= 86400

    @staticmethod
    def get_datetime_diff(var1: datetime, var2: datetime):
        """
            获取两个时间的 秒差
        :param var1:
        :param var2:
        :return:
        """
        diff = (var2 - var1).seconds
        day_diff = TimeUtils.get_datetime_diff_day(var1, var2)
        return day_diff * 3600 * 24 + diff

    @staticmethod
    def get_datetime_diff_day(var1: datetime, var2: datetime):
        """
            获取两个时间日期差
        :param var1:
        :param var2:
        :return:
        """
        return (var2.date() - var1.date()).days

    @staticmethod
    def get_end_of_week(var, _format: str = None) -> datetime:
        """
            获取一周结束时间
        :param var:
        :param _format:
        :return:
        """
        t = TimeUtils.get_begin_of_week(var, _format)
        if t is None:
            raise TimeConversionTypeError
        return TimeUtils.get_end_of_day(t + timedelta(days=6))

    @staticmethod
    def get_begin_of_week(var, _format: str = None) -> datetime:
        """
            获取一周开始时间
        :param var:
        :param _format:
        :return:
        """
        t = TimeUtils.get_begin_of_day(var, _format)
        if t is None:
            raise TimeConversionTypeError
        return t - timedelta(days=t.weekday())

    @staticmethod
    def get_end_of_month(var, _format: str = None) -> datetime:
        """
            获取月底时间
        :param var: 入参的类型 可以是 str ， datetime ， date ，  struct_time
        :param _format:
        :return:
        """
        t = TimeUtils.get_begin_of_month(var, _format)
        if t is None:
            raise TimeConversionTypeError
        t += timedelta(days=32)
        return TimeUtils.get_end_of_day(t - timedelta(days=t.day))

    @staticmethod
    def get_begin_of_month(var, _format: str = None) -> datetime:
        """
            获取月初时间
        :param var:入参的类型 可以是 str ， datetime ， date ，  struct_time
        :param _format:
        :return:
        """
        t = TimeUtils.get_begin_of_month(var, _format)
        if t is None:
            raise TimeConversionTypeError
        return TimeUtils.get_begin_of_day(datetime(year=t.year, month=t.month, day=1))

    @staticmethod
    def get_end_of_day(var, _format: str = None) -> datetime:
        """
            获取一天结束时间
        :param var:入参的类型 可以是 str ， datetime ， date ，  struct_time
        :param _format:
        :return:
        """
        t = TimeUtils.get_datetime(var, _format)
        if t is None:
            raise TimeConversionTypeError
        return t.replace(hour=23, minute=59, second=59)

    @staticmethod
    def get_begin_of_day(var, _format: str = None) -> datetime:
        """
            获取一天开始时间
        :param var:
        :param _format:
        :return:
        """
        t = TimeUtils.get_datetime(var, _format)
        if t is None:
            raise TimeConversionTypeError
        return t.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_datetime(var, _format: str = None):
        """
            时间转成 datetime
        :param var:
        :param _format:
        :return:
        """
        if var is None:
            raise NullPointError
        if isinstance(var, str):
            if _format is None:
                raise TimeNoFormatError
            return datetime.strptime(var, _format)
        elif isinstance(var, datetime):
            return var
        elif isinstance(var, time.struct_time):
            return datetime(year=var.tm_year, month=var.tm_mon, day=var.tm_mday, hour=var.tm_hour, minute=var.tm_min,
                            second=var.tm_sec)
        elif isinstance(var, date):
            return datetime(year=var.year, month=var.year, day=var.day)

    @staticmethod
    def get_timestamp(var=None, _format: str = None) -> int:
        """
            获取时间戳
        :param var: 时间 如果为空 表示获取当前时间的时间戳
        :param _format:  时间格式 , 当 var 是 str 的时候，需要传入
        :return:
        """
        t = datetime.now() if var is None else TimeUtils.get_datetime(var, _format)
        if t is None:
            raise TimeConversionTypeError
        # if var is None or isinstance(var, datetime):
        #     if var is None:
        #         timestamp = int(datetime.now().timestamp() * 1000)
        #     else:
        #         timestamp = int(var.timestamp() * 1000)
        # elif isinstance(var, str):
        #     if is_empty(_format):
        #         raise TimeNoFormatError()
        #     # 如果是字符串类型的时间格式 ， 必须有时间格式
        #     time_array = time.strptime(var, _format)
        #     timestamp = int(time.mktime(time_array))
        #     timestamp = timestamp * 1000
        # elif isinstance(var, date):
        #     timestamp = int(
        #         datetime(year=var.year, month=var.month, day=var.day, hour=0, minute=0, second=0).timestamp() * 1000)
        # else:
        #     raise TimeConversionTypeError
        return int(t.timestamp() * 1000)


import loguru

logger = loguru.logger
if __name__ == '__main__':
    try:
        a = {"a": "dadf", "bac": "xx", "a1": None}
        en = Entity(a)
        print(en.a1)
        v = TimeUtils.get_datetime(time.strptime("2022-03-26 03:00:00", TimeUtils.DATETIME_FORMAT_DEFAULT))
        v2 = TimeUtils.get_datetime(time.strptime("2023-03-29 11:24:50", TimeUtils.DATETIME_FORMAT_DEFAULT))
        logger.info(random.Random(TimeUtils.get_timestamp()).randrange(0, 999))
    except TimeNoFormatError as e:
        logger.exception(e)
