import kubernetes
from kubernetes import client, config
from jinja2 import Environment, FileSystemLoader
import yaml

config.load_kube_config()
core_v1 = client.CoreV1Api()

# List of namesopace
namespace = ['brown-dev-001']

def file_detail():
    filename = "../merge_yaml/dev-001.yaml"
    with open(filename, 'r') as file:
        file_list = list(yaml.safe_load_all(file))
        pvc_name = [name['metadata']['name'] for name in file_list if name['kind'] == 'PersistentVolumeClaim']
    # print(pvc_name)
    return pvc_name

def get_pvc_details(namespace,pvc_name):
    # print(namespace)
    pvc = core_v1.list_persistent_volume_claim_for_all_namespaces()
    pvc_list = list()
    for item in pvc.items:
        pvc_details = {}
        if item.metadata.namespace in namespace:
            if item.spec.access_modes[0] == 'ReadWriteMany' and item.metadata.name not in pvc_name:
                pvc_details['metadata'] = {}
                pvc_details['metadata']['name'] = item.metadata.name
                pvc_details['metadata']['namespace'] = item.metadata.namespace
                pvc_details['spec'] = {}
                pvc_details['spec']['resources'] = {}
                pvc_details['spec']['resources']['requests'] = {}
                pvc_details['spec']['resources']['requests']['storage'] = item.spec.resources.requests['storage']
                pvc_details['spec']['storageClassName'] = item.spec.storage_class_name
                pvc_details['spec']['volumeMode'] = item.spec.volume_mode
                pvc_details['spec']['volumeName'] = item.spec.volume_name
                pvc_list.append(pvc_details)
    # print(pvc_list)
    return pvc_list

def create_pvc_manifest(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('pvc_template.yaml.j2')
    rendered_yaml = template.render(all_claims=data)
    return rendered_yaml
    # print(rendered_yaml)
    # with open(filename, "w") as f:
    #     f.write(rendered_yaml)
    # print(f"YAML file {filename} generated successfully.")

def merge_pvc(pvc):
    filename = "../merge_yaml/dev-001.yaml"
    with open(filename, 'r') as file:
        existing_content = file.read()
    new_file = existing_content + pvc
    with open(filename, "w") as f:
        f.write(new_file)
        print(f"YAML file {filename} generated successfully.")


pvc_list = file_detail()
data = get_pvc_details(namespace,pvc_list)
pvc = create_pvc_manifest(data)
merge_pvc(pvc)
