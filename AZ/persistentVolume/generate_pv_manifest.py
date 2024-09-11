import kubernetes
from kubernetes import client, config
from jinja2 import Environment, FileSystemLoader
import yaml

config.load_kube_config()
core_v1 = client.CoreV1Api()

# List of namesopace
namespace = ['brown-dev-001']

def existing_pv_detial():
    filename = "../persistentVolumeClaim/merge_yaml/dev-001.yaml"
    with open(filename, 'r') as file:
        file_list = list(yaml.safe_load_all(file))
        pv_name = [name['metadata']['name'] for name in file_list if name['kind'] == 'PersistentVolume']
    print(pv_name)
    return pv_name

def list_pv(pv_name):
    pvc = core_v1.list_persistent_volume_claim_for_all_namespaces()
    pv_list = list()
    for item in pvc.items:
        if item.metadata.namespace in namespace and item.spec.access_modes[0] == 'ReadWriteMany' and item.spec.volume_name not in pv_name:
            pv_list.append(item.spec.volume_name)
    # print(pv_list)
    return pv_list


def new_pv_details(namespace,pv_name):
    pv = core_v1.list_persistent_volume()
    pv_list = []
    for item in pv.items:
        pv_details = {}
        if item.metadata.name in pv_name:
            pv_details['metadata'] = {}
            pv_details['metadata']['name'] = item.metadata.name
            pv_details['spec'] = {}
            pv_details['spec']['capacity'] = {}
            pv_details['spec']['capacity']['storage'] = item.spec.capacity['storage']
            pv_details['spec']['csi'] = {}
            pv_details['spec']['csi']['driver'] = item.spec.csi.driver
            pv_details['spec']['csi']['volumeAttributes'] = {}
            pv_details['spec']['csi']['volumeAttributes']['backendUUID'] = item.spec.csi.volume_attributes['backendUUID']
            pv_details['spec']['csi']['volumeAttributes']['internalName'] = item.spec.csi.volume_attributes['internalName']
            pv_details['spec']['csi']['volumeAttributes']['name'] = item.spec.csi.volume_attributes['name']
            pv_details['spec']['csi']['volumeAttributes']['protocol'] = item.spec.csi.volume_attributes['protocol']
            pv_details['spec']['csi']['volumeAttributes']['sk'] = item.spec.csi.volume_attributes['storage.kubernetes.io/csiProvisionerIdentity']
            pv_details['spec']['csi']['volumeHandle'] = item.spec.csi.volume_handle
            pv_details['spec']['storageClassName'] = item.spec.storage_class_name
            pv_details['spec']['volumeMode'] = item.spec.volume_mode
            pv_list.append(pv_details)
            # print(item.metadata.name)
            # print(item.spec.capacity['storage'])
            # print(item.spec.csi.driver)
            print(item.spec.csi.volume_attributes['backendUUID'])
            # print(item.spec.csi.volume_handle)
            # print(item.spec.storage_class_name)
            # print(item.spec.volume_mode)
    # print(pv_list)
    return(pv_list)

def create_pv_manifest(pv_data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('pv_template.yaml.j2')
    rendered_yaml = template.render(all_claims=pv_data)
    print(rendered_yaml)
    return rendered_yaml

def merge_pvc(pv):
    filename = "../persistentVolumeClaim/merge_yaml/dev-001.yaml"
    with open(filename, 'r') as file:
        existing_content = file.read()
    new_file = existing_content + pv
    with open(filename, "w") as f:
        f.write(new_file)
        print(f"YAML file {filename} generated successfully.")


old_pv_name = existing_pv_detial()
# new_pv_list = list_pv(old_pv_name)
# pv_data = new_pv_details(namespace,new_pv_list)
# pv = create_pv_manifest(pv_data)
# merge_pvc(pv)