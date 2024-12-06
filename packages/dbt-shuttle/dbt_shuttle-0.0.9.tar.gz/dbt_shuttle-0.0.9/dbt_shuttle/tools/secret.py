import json

from google.cloud import secretmanager


def get_secret_value(project_id, secret_name):
    client = secretmanager.SecretManagerServiceClient()

    secret_version_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=secret_version_name)
    secret_value = response.payload.data.decode('UTF-8')
    variables = json.loads(secret_value)
    variables['PROJECT_ID'] = project_id
    return variables
