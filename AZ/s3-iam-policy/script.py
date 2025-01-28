from kubernetes import client, config
from jinja2 import Environment, FileSystemLoader
import os

config.load_kube_config()

clusters = ["brown"]
# output_dir = 

# os.makedirs(output_dir, exist_ok=True)

def get_namespace():
    api_instance = client.CustomObjectsApi()
    profiles = api_instance.list_cluster_custom_object(group="kubeflow.org",version="v1",plural="profiles")
    namespace = [profile['metadata']['name'] for profile in profiles.get('items', [])]
    print(namespace)
    return namespace

def generate_iam_policy(profiles):
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("iam_template.j2")
    
    for profile in profiles:
        namespace = profile
        sort_name = "-".join(profile.split("-")[-2:])
        
        output_content = template.render(namespace=namespace, cluster="brown")
        output_path = os.path.join(output_dir, f"brown_{sort_name}.txt")
        with open(output_path, "w") as f:
            f.write(output_content)
        print(f"Generated: {output_path}")

    print("File generation complete!")
    
for cluster in clusters:
    output_dir = cluster
    os.makedirs(output_dir, exist_ok=True)
    
    profiles = get_namespace()
    policy = generate_iam_policy(profiles)
