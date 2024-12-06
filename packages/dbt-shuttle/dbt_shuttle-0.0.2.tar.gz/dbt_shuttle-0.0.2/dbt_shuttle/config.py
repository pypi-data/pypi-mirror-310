import json
import os
from dbt_shuttle.exceptions import EnvironmentVariableError


class Config:
    """全局配置类，管理项目配置和相关操作"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化全局配置"""
        self.project_id = None
        self.credentials = None
        self.working_dir = os.getcwd()

    def load_environment(self):
        """从环境变量加载配置"""
        self.credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not self.credentials:
            raise EnvironmentVariableError("缺少环境变量 'GOOGLE_APPLICATION_CREDENTIALS'，请配置后再运行命令。")

        try:
            with open(self.credentials, "r") as file:
                credentials = json.load(file)
                self.project_id = credentials.get("project_id")
        except Exception as e:
            raise EnvironmentVariableError(
                "从 'GOOGLE_APPLICATION_CREDENTIALS' 读取 'project_id'失败，请检查后再运行命令。")
        if not self.project_id:
            raise EnvironmentVariableError("GOOGLE_APPLICATION_CREDENTIALS缺少 'project_id'，请配置后再运行命令。")

    def validate_working_dir(self):
        """验证当前工作目录是否符合要求"""
        if not os.path.exists(self.working_dir):
            raise FileNotFoundError(f"工作目录不存在：{self.working_dir}")

    def reset(self, working_dir=None):
        """重置配置，允许更改工作目录"""
        self.working_dir = working_dir or os.getcwd()

    @staticmethod
    def get_instance():
        """获取全局配置对象"""
        if not Config._instance:
            raise RuntimeError("Config 未初始化，请先调用 Config().load_environment()。")
        return Config._instance

    def __repr__(self):
        return (f"Config(project_id={self.project_id}, "
                f"credentials={self.credentials}, "
                f"working_dir={self.working_dir})")
