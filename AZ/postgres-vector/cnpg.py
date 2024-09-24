from jinja2 import Environment, FileSystemLoader
import os

NAMESPACE = 'brown-dev-001'
CLUSTER = 'dev'
if CLUSTER == 'dev':
    CLUSTER = 'brown'
if CLUSTER == 'mirror':
    BUCKET_NAME = 'az-eu-azimuth-kfp-afe'
else:
    BUCKET_NAME = f"az-eu-azimuth-kfp-{CLUSTER}"
NUMBER_INSTANCE = 3
IMAGE_VERSION = '16.4'
PVC_STORAGE_SIZE = 100
AWS_REGION = "eu-west-1"
WAL_STORAGE = 20
REQUEST_MEMORY = "512Mi"
REQUEST_CPU = "1"
LIMITS_MEMORY = "1Gi"
LIMITS_CPU = "2"

env = Environment(loader=FileSystemLoader("./"))
templates = env.get_template("cnpg.yaml.j2")
content = templates.render(
    cluster = CLUSTER,
    namespace = NAMESPACE,
    number_instance = NUMBER_INSTANCE,
    cnpg_image_version = IMAGE_VERSION,
    pvc_storage_size = PVC_STORAGE_SIZE,
    aws_s3_bucket = BUCKET_NAME,
    aws_bucket_region = AWS_REGION,
    wal_storage_size = WAL_STORAGE,
    request_memory = REQUEST_MEMORY,
    request_cpu = REQUEST_CPU,
    limits_memory = LIMITS_MEMORY,
    limits_cpu = LIMITS_CPU
)

filename = f"cnpg.yaml"

with open(filename,'w') as f:
    f.write(content)
    print(f"cnpg manifest file {filename} created.")