class DBTShuttleException(Exception):
    """通用异常基类"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EnvironmentVariableError(DBTShuttleException):
    """环境变量相关异常"""
    pass


class DirectoryError(DBTShuttleException):
    """目录结构错误"""
    pass


class SecretManagerError(DBTShuttleException):
    """Google Secret Manager 相关异常"""
    pass

class FileReaderError(DBTShuttleException):
    """读取文件相关异常"""
    pass
