from kubernetes import config, client
from jinja2 import Environment, FileSystemLoader
import os
import argparse


def get_namespace():
    api_instance = client.CustomObjectsApi()
    profiles = api_instance.list_cluster_custom_object(group="kubeflow.org",version="v1",plural="profiles")
    namespace = [profile['metadata']['name'] for profile in profiles.get('items', [])]
    return namespace

def generate_iam_policy(*args):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    
    for profile in profiles:
        namespace = profile
        if cluster == "dev":
            sort_name = "-".join(profile.split("-")[-2:])
            file_name = f"brown-{sort_name}"
        else:
            sort_name = profile.split('-')
            if cluster not in sort_name:
                file_name = f"{cluster}-{profile}"
            else:
                sort_namespace = "-".join(sort_name[-2:])
                file_name = f"{cluster}-{sort_namespace}"

        output_content = template.render(namespace=namespace, cluster=cluster)
        output_path = os.path.join(output_dir, f"{file_name}.txt")
        with open(output_path, "w") as f:
            f.write(output_content)

parser = argparse.ArgumentParser(description="Getting Detials from Github Ation")
parser.add_argument("-c", "--clusterName", help="cluster_name")
args = parser.parse_args()
args = vars(args)
cluster = args["clusterName"]
clusters = cluster.split(",")

for cluster in clusters:
    output_dir = f"../policy/{cluster}"
    template_dir = "../templates"
    template_file = "iam_policy_template.j2"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if cluster == 'dev':
        config.load_kube_config(config_file=os.environ['KUBECONFIG'],context='ai-ops-brown@kubernetes')
    else:
        config.load_kube_config(config_file=os.environ['KUBECONFIG'],context=f"ai-ops-{cluster}@kubernetes")
        
    profiles = get_namespace()
    policy = generate_iam_policy(template_dir, template_file, profiles, cluster)    