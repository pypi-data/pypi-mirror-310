import json
import logging
import os
import re
import shutil

import yaml

from dbt_shuttle.config import Config
from dbt_shuttle.exceptions import DirectoryError, FileReaderError
from dbt_shuttle.tools import secret

logger = logging.getLogger(__name__)


# Utility Functions
def get_key_by_value(d, target_value):
    """Find the first key in the dictionary where the value matches target_value."""
    return next((k for k, v in d.items() if v == target_value), None)


def value_in_dicts(target_value, list_of_dicts):
    """Check if target_value is present in any dictionary within a list of dictionaries."""
    return any(target_value in d.values() for d in list_of_dicts)


def flatten_dict_values(data):
    """Flatten values from nested dictionaries, excluding keys with 'tables'."""
    flat_set = set()

    def flatten(value, key=None):
        if isinstance(value, str):
            flat_set.add(value)
        elif isinstance(value, list):
            for item in value:
                flatten(item)
        elif isinstance(value, dict):
            for k, v in value.items():
                if 'tables' not in k:
                    flatten(v, k)

    flatten(data)
    return flat_set


# DBT Config Functions
def read_dbt_config(model_folder):
    """Read the schema configuration from schema.yml in the DBT models folder."""
    schema_path = os.path.join(model_folder, 'schema.yml')

    try:
        with open(schema_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise FileReaderError(f"读取DBT schema.yml: {schema_path} 异常.")


def generate_dataset(schema, table, source_config):
    """Generate the dataset name based on schema and table names using schema config."""
    for config in source_config:
        if schema == config['name'] and value_in_dicts(table, config['tables']):
            return config['database']
    raise ValueError(f"Dataset for schema '{schema}' and table '{table}' not found.")


# SQL Transformation Functions
def replace_refs(text):
    """Replace {{ ref('TABLE') }} syntax in SQL text with the fully-qualified table name."""
    pattern = r"\{\{\s*ref\('([^']+)'\)\s*\}\}"

    def replace_match(match):
        table = match.group(1)
        return f"`{{{{ PROJECT_ID }}}}.{{{{ REVENUE_CALCULATION_DATASET }}}}.{table}`"

    return re.sub(pattern, replace_match, text)


def replace_sources(text, dbt_var_mapping, source_config):
    """Replace {{ source('SCHEMA', 'TABLE') }} syntax in SQL text with the fully-qualified source name."""
    pattern = r"\{\{\s*source\('([^']+)',\s*'([^']+)'\)\s*\}\}"

    def replace_match(match):
        schema = match.group(1)
        table = match.group(2)
        dataset = get_key_by_value(dbt_var_mapping, generate_dataset(schema, table, source_config))
        return f"`{{{{ {dataset} }}}}.{{{{ {get_key_by_value(dbt_var_mapping, schema)} }}}}.{table}`"

    return re.sub(pattern, replace_match, text)


# File Operations
def move_and_prepare_sql_files(model_folder, output_folder):
    """Move SQL files to the output folder, resetting the output folder."""
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder)
    shutil.copytree(model_folder, output_folder, dirs_exist_ok=True)


def update_sql_files(output_folder, dbt_var_mapping, source_config):
    """Update SQL files in the output folder by replacing references and sources."""
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.sql'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r+', encoding='utf-8') as sql_file:
                    next(sql_file)  # Skip the first line
                    content = sql_file.read()
                    new_sql = replace_sources(replace_refs(content), dbt_var_mapping, source_config)
                    sql_file.seek(0)
                    sql_file.write(new_sql)
                    sql_file.truncate()


def execute(secret_name):
    """执行 end_work 逻辑"""
    logger.info("~ ） end_work 准备就绪！")

    # Directory paths
    config = Config.get_instance()
    working_dir = config.working_dir
    project_id = config.project_id

    parent_dir = os.path.dirname(working_dir)
    dbt_project_dir = os.path.join(parent_dir, "dbt")
    vars_config_path = os.path.join(parent_dir, 'vars.yml')
    model_folder = os.path.join(dbt_project_dir, "models")
    output_folder = os.path.join(dbt_project_dir, "sql")

    if not os.path.isdir(dbt_project_dir) or not os.path.isdir(model_folder):
        raise DirectoryError(f"目录: {dbt_project_dir} 或者 {model_folder}不存在.")

    # Load schema configuration and flatten dictionary values
    source_config = read_dbt_config(model_folder)['sources']
    dbt_var_set = flatten_dict_values(source_config)

    # Get secret variables and filter by relevant DBT variables
    variables = secret.get_secret_value(project_id, secret_name)

    if os.path.exists(vars_config_path):
        with open(vars_config_path, 'r') as file:
            variables.update(yaml.safe_load(file))

    dbt_var_mapping = {k: v for k, v in variables.items() if isinstance(v, str) and v in dbt_var_set}

    # Move files and apply SQL transformations
    move_and_prepare_sql_files(model_folder, output_folder)
    update_sql_files(output_folder, dbt_var_mapping, source_config)

    logger.info("：） end_work 完成！下班！！")
