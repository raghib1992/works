from jinja2 import Environment, FileSystemLoader

CLUSTER = os.environ['CLUSTER']
NAMESPACE = os.environ['NAMESPACE']
MILVUS_IMAGE_VERSION = os.environ['MILVUS_IMAGE_VERSION']
BUCKET_NAME = os.environ['BUCKET_NAME']
ATTU_IMAGE_VERSION = os.environ['ATTU_IMAGE_VERSION']

env = Environment(loader=FileSystemLoader("."))
templates = env.get_template("milvus_template.yaml.j2")

content = templates.render(
    cluster = CLUSTER,
    namespace = NAMESPACE,
    milvus_image_version =  MILVUS_IMAGE_VERSION,
    bucket_name = BBUCKET_NAME,
    attu_image_version = ATTU_IMAGE_VERSION
)

with open('milvus-dev-001.yaml','w') as f:
    f.write(content)
    print(f"milvus manifest file created.")
