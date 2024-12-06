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
    """
    从datashuttle的SQL代码导入到dbt的工程代码，一天的工作从这里开始吧~


    位置参数:
        your_secret_name        用于替换data-shuttle工程SQL中的变量，在当前目录添加[vars.yml]可增加/更新变量值.
        your_dataset_name       DBT工程中用到的默认数据集.

    输出结果：
        在当前目录下生成一个dbt目录，此为dbt工程，可以直接在这个目录下运行dbt的命令，也可以添加单元测试、数据测试、文档描述等内容
    """
    try:
        begin_work.execute(secret_name, dataset)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


@cli.command("end_work")
@click.argument("secret_name")
def export_command(secret_name):
    """
    从dbt的工程代码导入到datashuttle的SQL代码，今天的工作就到这里吧~


    位置参数:
        your_secret_name        用于将DBT工程SQL中的变量恢复为data-shuttle工程，在当前目录添加[vars.yml]可增加/更新变量值.

    输出结果：
        在dbt目录生成一个sql目录，其内容为将DBT工程model下的SQL恢复为data-shuttle工程的SQL
    """
    try:
        end_work.execute(secret_name)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


@cli.command("show_work")
@click.argument("domain")
def index_command(domain):
    """
    更新GCS bucket文件，返回可直接打开的GCS URL


    位置参数:
        your_domain_name   用于做BUCKET下目录的区分.

    输出结果：
        会在GCS dbt_revenue_forecast这个BUCKET下生成DBT工程的网页文件，同时打印访问链接
    """
    try:
        show_work.execute(domain)
    except DBTShuttleException as e:
        logger.error(f"错误: {e.message}")


if __name__ == "__main__":
    cli()
