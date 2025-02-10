from jinja2 import Environment, FileSystemLoader
import os
import string
import random
import base64
import hvac
import sys

def generate_random_password(length):
    character_set = string.digits + string.ascii_letters 
    password = ''.join(random.choice(character_set) for _ in range(length))
    return password

def update_vault(clusterName, namespace, secret_data):
    try:
        client = hvac.Client(
            url='https://vault.cna.astrazeneca.net',
        )

        client.auth.userpass.login(
            username = os.environ['VAULT_USERNAME'],
            password = os.environ['VAULT_PASSWORD']
        )

        client.secrets.kv.v2.create_or_update_secret(
            path=f'{clusterName}/cnpg/{namespace}', 
            mount_point='aiops',
            secret=secret_data,
        )
    except Exception as e:
        print(e)
        sys.exit(1)
    
NAMESPACE = os.environ['NAMESPACE']
CLUSTER = os.environ['CLUSTER']
if CLUSTER == 'dev':
    SORT_CLUSTER = 'brown'
    SORT_NAMESPACE = "-".join(NAMESPACE.split("-")[-2:])
else:
    SORT_NAMESPACE = NAMESPACE.split("-")
    SORT_CLUSTER = CLUSTER
    if CLUSTER in SORT_NAMESPACE:
        SORT_NAMESPACE = "-".join(NAMESPACE.split("-")[-2:])
    else:
        SORT_NAMESPACE = NAMESPACE
if CLUSTER == 'mirror':
    BUCKET_NAME = 'az-eu-azimuth-kfp-afe'
else:
    BUCKET_NAME = f"az-eu-azimuth-kfp-{CLUSTER}"
NUMBER_INSTANCE = os.environ['NUMBER_INSTANCE']
IMAGE_VERSION = os.environ['IMAGE_VERSION']
PVC_STORAGE_SIZE = os.environ['PVC_STORAGE_SIZE']
AWS_REGION = os.environ['AWS_REGION']
REQUEST_MEMORY = os.environ['MEMORY']
REQUEST_CPU = os.environ['CPU']
LIMITS_MEMORY = os.environ['MEMORY']
LIMITS_CPU = os.environ['CPU']
WAL_STORAGE = int(float(PVC_STORAGE_SIZE) * 0.2)
CNPG_APP_USERNAME = "app"
CNPG_APP_PASSWORD = generate_random_password(14)
ENCODED_CNPG_APP_USERNAME = base64.b64encode(CNPG_APP_USERNAME.encode('utf-8')).decode('utf-8')
ENCODED_CNPG_APP_PASSWORD = base64.b64encode(CNPG_APP_PASSWORD.encode('utf-8')).decode('utf-8')
CNPG_SU_PASSWORD = generate_random_password(14)
CNPG_SU_NAME = "postgres"
ENCODED_CNPG_SU_NAME = base64.b64encode(CNPG_SU_NAME.encode('utf-8')).decode('utf-8')
ENCODED_CNPG_SU_PASSWORD = base64.b64encode(CNPG_SU_PASSWORD.encode('utf-8')).decode('utf-8')
SCHEDULEBACK_TIME = os.environ['SCHEDULEBACK_TIME']
if SCHEDULEBACK_TIME == 'Daily':
    ScheduleBackupTime = "0 0 0 * * *"
elif SCHEDULEBACK_TIME == 'Weekly':
    ScheduleBackupTime = "0 0 0 * * 0"
elif SCHEDULEBACK_TIME == 'Monthly':
    ScheduleBackupTime = "0 0 0 1 * *"
PGADMIN_USER = os.environ['PGADMIN_USER']
PGADMIN_PASSWORD = generate_random_password(14)
PGADMIN_IMAGE_VERSION = os.environ['PGADMIN_IMAGE_VERSION']
ENCODED_PGADMIN_USER = base64.b64encode(PGADMIN_USER.encode('utf-8')).decode('utf-8')
ENCODED_PGADMIN_PASSWORD = base64.b64encode(PGADMIN_PASSWORD.encode('utf-8')).decode('utf-8')

env = Environment(loader=FileSystemLoader("../templates"))
templates = env.get_template("cnpg_template.yaml.j2")
content = templates.render(
    cluster = SORT_CLUSTER,
    namespace = NAMESPACE,
    sort_namespace = SORT_NAMESPACE,
    number_instance = NUMBER_INSTANCE,
    cnpg_image_version = IMAGE_VERSION,
    pvc_storage_size = PVC_STORAGE_SIZE,
    aws_s3_bucket = BUCKET_NAME,
    aws_bucket_region = AWS_REGION,
    wal_storage_size = WAL_STORAGE,
    request_memory = REQUEST_MEMORY,
    request_cpu = REQUEST_CPU,
    limits_memory = LIMITS_MEMORY,
    limits_cpu = LIMITS_CPU,
    cnpg_superuser_name = ENCODED_CNPG_SU_NAME,
    cnpg_superuser_password = ENCODED_CNPG_SU_PASSWORD,
    cnpg_app_username = ENCODED_CNPG_APP_USERNAME,
    cnpg_app_password = ENCODED_CNPG_APP_PASSWORD,
    schedule_backup_time = ScheduleBackupTime,
    pgAdmin_password = ENCODED_PGADMIN_PASSWORD,
    pgadmin_image_version = PGADMIN_IMAGE_VERSION,
    pgadmin_user = ENCODED_PGADMIN_USER
)

filename = f"../cnpg-db/{CLUSTER}/{NAMESPACE}.yaml"

with open(filename,'w') as f:
    f.write(content)
    print(f"Created cnpg manifest file: {filename}")
    
    
# Update Password in vault
SECRET_DATA = {
    'cnpg_super_username': f"{CNPG_SU_NAME}",
    'cnpg_superuser_password': f"{CNPG_SU_PASSWORD}",
    'cnpg_app_username': f"{CNPG_APP_USERNAME}",
    'cnpg_app_password' : f"{CNPG_APP_PASSWORD}",
    'pgAdmin_password' : f"{PGADMIN_PASSWORD}",
    'pgadmin_user' : f"{PGADMIN_USER}"
}
update_vault(CLUSTER, NAMESPACE, SECRET_DATA)