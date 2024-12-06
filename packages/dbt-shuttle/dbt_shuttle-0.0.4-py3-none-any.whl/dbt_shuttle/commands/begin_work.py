import logging
import os
import re
import shutil
import textwrap
from collections import defaultdict

import yaml

from dbt_shuttle.config import Config
from dbt_shuttle.exceptions import DirectoryError
from dbt_shuttle.tools import secret

logger = logging.getLogger(__name__)


def create_dbt_project_structure(project_dir):
    shutil.rmtree(project_dir, ignore_errors=True)
    os.makedirs(project_dir)

    for dir_name in ['models']:
        full_path = os.path.join(project_dir, dir_name)
        os.makedirs(full_path, exist_ok=True)


def get_ori_sql(dst, variables):
    def find_variables(sql_content):
        pattern = re.compile(r'\{\{ (.*?) \}\}')
        return set(match.group(1) for match in pattern.finditer(sql_content))

    def replace_variables(sql_content, variables):
        for var_name, var_value in variables.items():
            pattern = re.compile(r'\{\{ ' + re.escape(var_name) + r' \}\}')
            sql_content = pattern.sub(str(var_value), sql_content)
        sql_content = sql_content.replace("DATETIME('{{ NOW_DATETIME }}')", "CURRENT_DATETIME")
        return sql_content

    variable_error_flag = False
    for root, dirs, files in os.walk(dst):
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as sql_file:
                    sql_content = sql_file.read()
                with open(file_path, 'w', encoding='utf-8') as output_file:
                    sql_content = replace_variables(sql_content, variables)
                    output_file.write(sql_content)
                remaining_variables = find_variables(sql_content) - set(variables.keys())
                if remaining_variables:
                    variable_error_flag = True
                    logging.warning(f"警告：{file_path}以下变量未被替换:")
                    for var in remaining_variables:
                        logging.warning(f"variables['{var}'] = ''")
    if variable_error_flag:
        raise Exception('变量未被完全替换')


def get_dbt_sql(dst, project_id):
    sources_dict = defaultdict(set)

    def replacement_function(match):
        table_name = match.group(1)
        return f"{{{{ ref('{table_name}') }}}}"

    def update_content(content):

        prefix = f'{project_id}.revenue_calculation_v3'
        suffix_pattern = r'([A-Za-z0-9_]+)'
        pattern_to_replace = rf'`{re.escape(prefix)}\.{suffix_pattern}`'
        pattern_to_print = r'`([^`]*)`'
        new_content = re.sub(pattern_to_replace, replacement_function, content)
        matches = re.findall(pattern_to_print, new_content)
        for match in matches:
            if len(match.split('.')) == 3:
                db, schema, table = match.split('.')
                formatted_string = f"{{{{ source('{schema}', '{table}') }}}}"
                key = f"{db}.{schema}"
                sources_dict[key].add(table)
                new_content = re.sub(rf"`{db}\.{schema}\.{table}`", formatted_string, new_content)
        return new_content

    for root, dirs, files in os.walk(dst):
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as sql_file:
                    content = sql_file.read()
                new_content = update_content(content)
                with open(file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(f'{{{{ config(tags = ["{os.path.basename(root)}"]) }}}}\n' + new_content)
    return sources_dict


def write_project_config(project_dir, dbt_project_name):
    dbt_project_content = textwrap.dedent(f"""
    name: '{dbt_project_name}'
    version: '1.0.0'
    profile: '{dbt_project_name}-profile'
    models:
        {dbt_project_name}:
            +materialized: table
    """)
    with open(os.path.join(project_dir, 'dbt_project.yml'), 'w') as file:
        file.write(dbt_project_content)


def write_profiles_config(project_dir, dbt_project_name, dataset):
    config = Config.get_instance()
    credential_path = config.credentials
    project_id = config.project_id
    profiles_content = textwrap.dedent(f"""
    {dbt_project_name}-profile:
      target: dev
      outputs:
        dev:
          dataset: {dataset}
          job_execution_timeout_seconds: 300
          job_retries: 1
          keyfile: {credential_path}
          location: US
          method: service-account
          priority: interactive
          project: {project_id}
          threads: 2
          type: bigquery
    """)
    with open(os.path.join(project_dir, 'profiles.yml'), 'w') as file:
        file.write(profiles_content)


def write_schema_config(model_folder, sources_dict):
    with open(os.path.join(model_folder, 'schema.yml'), "w") as f:
        f.write("version: 2\n")
        f.write("sources:\n")
        for key, tables in sources_dict.items():
            f.write(f"    - name: {key.split('.')[1]}\n")
            f.write(f"      database: {key.split('.')[0]}\n")
            f.write("      tables:\n")
            for table in tables:
                f.write(f"         - name: {table}\n")


def execute(secret_name, dataset):
    """执行 begin_work 逻辑"""
    logger.info("~ ） begin_work 准备就绪！")

    # Directory paths
    config = Config.get_instance()
    working_dir = config.working_dir
    project_id = config.project_id
    parent_dir = os.path.dirname(working_dir)
    dbt_project_name = os.path.basename(parent_dir)
    sql_dir = os.path.join(parent_dir, 'sql')
    project_dir = os.path.join(parent_dir, 'dbt')
    vars_config_path = os.path.join(parent_dir, 'vars.yml')

    model_folder = os.path.join(project_dir, 'models')

    if not os.path.isdir(sql_dir):
        raise DirectoryError(f"目录: {sql_dir} 不存在, begin_work失败.")

    variables = secret.get_secret_value(project_id, secret_name)

    if os.path.exists(vars_config_path):
        with open(vars_config_path, 'r') as file:
            variables.update(yaml.safe_load(file))

    create_dbt_project_structure(project_dir)
    shutil.copytree(sql_dir, model_folder, dirs_exist_ok=True)
    get_ori_sql(model_folder, variables)
    sources_dict = get_dbt_sql(model_folder, project_id)

    # Configure dbt project
    write_project_config(project_dir, dbt_project_name)
    write_profiles_config(project_dir, dbt_project_name, dataset)
    write_schema_config(model_folder, sources_dict)

    os.chdir(project_dir)
    os.system('dbt deps')
    # os.system('dbt run --full-refresh')
    os.system('dbt test')
    os.system('dbt docs generate')

    logger.info("：） begin_work 完成！今日进度50%！！")
    os.system('dbt docs serve')
