import json
import logging
import os
import re

from google.cloud import storage

from dbt_shuttle.config import Config
from dbt_shuttle.exceptions import DirectoryError

logger = logging.getLogger(__name__)


def upload_to_gcs(bucket_name, source_file_path, domain):
    destination_blob_name = f"{domain}/index2.html"
    try:
        client = storage.Client()

        bucket = client.get_bucket(bucket_name)

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)

        print(
            f"文件 {source_file_path} 已成功上传到存储桶 {bucket_name}，路径为 {destination_blob_name}\n 文件url为 "
            f"https://storage.cloud.google.com/{bucket_name}/{domain}/index2.html?authuser=1")
    except Exception as e:
        print(f"上传文件时发生错误: {e}")


def execute(domain):
    """执行 show_work 逻辑"""
    # Directory paths
    config = Config.get_instance()
    working_dir = config.working_dir
    parent_dir = os.path.dirname(working_dir)
    path_dbt_project = os.path.join(parent_dir, 'dbt')
    dbt_target_path = os.path.join(path_dbt_project, 'target')
    bucket_name = 'dbt_revenue_forecast'

    if not dbt_target_path:
        raise DirectoryError(f"当前 dbt 目录: {path_dbt_project} 缺少 'target' 文件夹.")

    search_str = 'n=[o("manifest","manifest.json"+t),o("catalog","catalog.json"+t)]'

    with open(os.path.join(dbt_target_path, 'index.html'), 'r') as f:
        content_index = f.read()

    with open(os.path.join(dbt_target_path, 'manifest.json'), 'r') as f:
        json_manifest = json.loads(f.read())

    ignore_projects = ['dbt', 'dbt_bigquery']
    for element_type in ['nodes', 'sources', 'macros', 'parent_map', 'child_map']:
        for key in list(json_manifest.get(element_type, {}).keys()):
            for ignore_project in ignore_projects:
                if re.match(fr'^.*\.{ignore_project}\.', key):
                    del json_manifest[element_type][key]

    with open(os.path.join(dbt_target_path, 'catalog.json'), 'r') as f:
        json_catalog = json.loads(f.read())

    with open(os.path.join(dbt_target_path, 'index2.html'), 'w') as f:
        new_str = "n=[{label: 'manifest', data: " + json.dumps(
            json_manifest) + "},{label: 'catalog', data: " + json.dumps(json_catalog) + "}]"
        new_content = content_index.replace(search_str, new_str)
        f.write(new_content)

    local_file_path = os.path.join(dbt_target_path, 'index2.html')

    upload_to_gcs(bucket_name, local_file_path, domain)

    logger.info("show_work 完成！")
