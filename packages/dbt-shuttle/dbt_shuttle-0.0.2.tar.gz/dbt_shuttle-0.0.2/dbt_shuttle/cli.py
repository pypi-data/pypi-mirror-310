import logging

import click

from dbt_shuttle.config import Config
from dbt_shuttle.exceptions import DBTShuttleException, EnvironmentVariableError
from dbt_shuttle.commands import begin_work, end_work, show_work

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def with_config(f):
    """装饰器：初始化全局 Config 对象并传递给命令函数"""

    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        config = ctx.ensure_object(Config)
        logger.info(f"当前配置: {config}")
        return ctx.invoke(f, config, *args, **kwargs)

    return wrapper


@click.group()
def cli():
    """dbt-shuttle 命令行工具"""
    try:
        config = Config()
        config.load_environment()
        config.validate_working_dir()
        logger.info("全局配置加载成功。")
    except EnvironmentVariableError as e:
        logger.error(f"启动失败: {e.message}")
        exit(1)
    except Exception as e:
        logger.error(f"未知错误: {e}")
        exit(1)


@cli.command("begin_work")
@click.argument("secret_name")
@click.argument("dataset")
def import_command(secret_name, dataset):
    """从datashuttle的SQL代码导入到dbt的工程代码"""
    try:
        begin_work.execute(secret_name, dataset)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


@cli.command("end_work")
@click.argument("secret_name")
def export_command(secret_name):
    """从dbt的工程代码导入到datashuttle的SQL代码"""
    try:
        end_work.execute(secret_name)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


@cli.command("show_work")
@click.argument("domain")
def index_command(domain):
    """更新GCS bucket文件，返回可视化 URL"""
    try:
        show_work.execute(domain)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


if __name__ == "__main__":
    cli()
