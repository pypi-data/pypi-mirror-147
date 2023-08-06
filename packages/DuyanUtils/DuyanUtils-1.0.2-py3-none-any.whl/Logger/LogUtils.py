import os

import loguru

TRACE = "TRACE"
INFO = "INFO"
DEBUG = "DEBUG"
ERROR = "ERROR"
WARNING = "WARNING"
fmt = "[%(thread)d]-[%(levelname)s]-[%(asctime)s}]-[%(process)d]-[%(name)s]-[%(funcName)s]%(lineno)s :%(message)s"


class Logger(object):
    LOGURU_FORMAT = loguru._defaults.env(
        "LOGURU_FORMAT",
        str,
        "[{process}]-"
        "[<level>{level: <8}</level>]-"
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>]-"
        "[<cyan>{thread}</cyan>]-"
        "[<cyan>{file}</cyan>]-"
        "[<cyan>{function}</cyan>]<cyan>{line}</cyan> :"
        "<level>{message}</level>",
    )
    LOGURU_ERROR_FORMAT = loguru._defaults.env(
        "LOGURU_FORMAT",
        str,
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{process} | {thread}</cyan> | "
        "<cyan>{file}</cyan>-><cyan>{function}</cyan>:<cyan>{line}</cyan> ]"
        "<level>{message}</level>",
    )

    @staticmethod
    def get_logger(file_name, project_name: str = None):
        """
            创建日志
        :param file_name:  保存日志文件名称 ，
        :param project_name:
        :return:
        """
        file_parent_path = "/var/log/duyansoft/py3log"
        if project_name:
            file_parent_path += ("/" + project_name)
        if not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path, exist_ok=True)
        info_file_path = f"{file_parent_path}/{file_name}-{INFO}.log"
        error_file_path = f"{file_parent_path}/{file_name}-{ERROR}.log"
        return Logger.get_logger_init(info_file_path, error_file_path, project_name=project_name)

    @staticmethod
    def get_logger_init(info_file_path, error_file_path, _format=LOGURU_FORMAT, level=INFO, rotation="12:00",
                        retention="3 days",
                        compression="zip", enqueue=False, project_name: str = None):
        logger_obj = loguru.logger

        logger_obj.add(info_file_path, format=_format, level=level, enqueue=enqueue, rotation=rotation,
                       retention=retention, compression=compression)
        # 错误日志默认保存三十天 错误日志格式和保存时间是无法配置的
        logger_obj.add(error_file_path, format=Logger.LOGURU_FORMAT, level=ERROR, enqueue=enqueue,
                       rotation=rotation, retention="30 days", compression=compression)
        return logger_obj

