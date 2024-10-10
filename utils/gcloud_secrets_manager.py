from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the secret from Google Cloud Secret Manager.

    :param project_id: Your GCP project ID.
    :param secret_id: The ID of the secret you want to access.
    :param version_id: The version of the secret (defaults to 'latest').
    :return: The secret payload as a string.
    """
    # Create a client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})

    # Extract the secret payload
    secret_payload = response.payload.data.decode("UTF-8")

    print(secret_payload)

    return secret_payload


def cloudbuild_yaml_string_parce(yaml_string: str, project_id: str) -> dict:

    secret_dict = {}
    secret_strings = []
    secret_keys = []
    yaml_string = yaml_string.replace(",", "=")
    yaml_list = yaml_string.split("=")

    for _ in yaml_list:
        if ":" in _:
            secret_string = _.split(":")
            secret_string = access_secret_version(project_id=project_id, secret_id=secret_string[0], version_id=secret_string[1])
            secret_strings.append(secret_string)
        else:
            secret_keys.append(_)
    
    for _ in range(len(secret_strings)):
        secret_dict[secret_keys[_]]=secret_strings[_]
    print(secret_dict)


cloudbuild_yaml_string_parce("KEY=dash_app_deployment_aws_key:3,SECRET=dash_app_deployment_aws_secret:3,DBNAME=dash_app_deployment_dbname:1,GOOGLE_APPLICATION_CREDENTIALS=dash_app_deployment_google_application_credentials:1,HOST=dash_app_deployment_host:1,PASSWORD=dash_app_deployment_password:1,ROS_HASH_KEY=dash_app_deployment_ros_hash_key:1,SECRET_KEY=dash_app_deployment_secret_key:1,USER=dash_app_deployment_user:1", "p3-prod-aa94d")

