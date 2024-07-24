# This is Python SDK script to connect with milvus-core db using root user
# It also retrieve milvus db credential from k8s secret (k8s secret pull password from Vault) to connect to db

from pymilvus import MilvusClient, connections
from kubernetes import client, config
import base64


# Load the Kubernetes configuration (in-cluster) to connect python-api to kubernetes using your kubeconfig file
config.load_kube_config(config_file="Path/to/kubeconfigfile")
v1 = client.CoreV1Api()
secret_name = "milvus-root-credential"
namespace = "milvus-operator"

# # Retrieve the secret object
secret = v1.read_namespaced_secret(secret_name, namespace)
password_data = secret.data["ROOT_CREDENTIAL"]
password = base64.b64decode(password_data).decode("utf-8")

# Milvus client to establish a connection
client = MilvusClient(
  uri='http://localhost:61356', # replace with your own Milvus server address
  token=f"root:{password}"
#   token='root:milvus123'
)

user = client.list_users()
print(user)

# To create new user uncomment below line and connect with AI team to create password and store in vault
# client.create_user(
#   user_name='nithin',
#   password='nithin123'
# )

user = client.list_users()
print(user)

# To Update password of exisitng user(uncomment below line)
# client.update_password(
#   user_name='nithin',
#   old_password='nithin123',
#   new_password='P@ssw0rd123'
# )