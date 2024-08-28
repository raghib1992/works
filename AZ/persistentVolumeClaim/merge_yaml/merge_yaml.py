import yaml


data = [
    {'apiVersion': 'v1', 'kind': 'PersistentVolumeClaim', 'metadata': {'finalizers': ['kubernetes.io/pvc-protection'], 'name': 'datavol-openvaccine-dataset', 'namespace': 'brown-dev-001'}, 'spec': {'accessModes': ['ReadWriteMany'], 'resources': {'requests': {'storage': '10Gi'}}, 'storageClassName': 'ontap-silver', 'volumeMode': 'Filesystem', 'volumeName': 'pvc-2051e61c-b63f-4039-a0ce-e1a43d623de8'}}, {'apiVersion': 'v1', 'kind': 'PersistentVolumeClaim', 'metadata': {'finalizers': ['kubernetes.io/pvc-protection'], 'name': 'shared-brown-dev-001', 'namespace': 'brown-dev-001'}, 'spec': {'accessModes': ['ReadWriteMany'], 'resources': {'requests': {'storage': '4Gi'}}, 'storageClassName': 'fsx-ontap-silver', 'volumeMode': 'Filesystem', 'volumeName': 'pvc-8bac86ff-d59e-44c2-bdee-25b7d501e1de'}}
]

# Load the existing YAML file
with open('dev-001.yaml', 'r') as file:
    old_dev_001 = list(yaml.safe_load_all(file))
    existing_pvc_name = [name['metadata']['name'] for name in old_dev_001 if name['kind'] == 'PersistentVolumeClaim']

# print(old_dev_001)
print(existing_pvc_name)

for pvc in data:
    if pvc['metadata']['name'] not in existing_pvc_name:
        print(pvc)
# for old_pvc in dev_001_list:
#     if old_pvc['kind'] == 'PersistentVolumeClaim' :
# #         print(old_pvc['metadata']['name'])
#     # print(old_pvc['kind'])
# required_pvc = []
# for new_pvc in data:
#     # print(new_pvc['metadata']['name'])
#     for old_pvc in dev_001_list:
#         if old_pvc['kind'] == 'PersistentVolumeClaim' and new_pvc['metadata']['name'] != old_pvc['metadata']['name']:
#             # print(new_pvc)
#             required_pvc = list(new_pvc.items())

# print(required_pvc)
# dev_001 = dev_001_list + required_pvc  
# print(dev_001)  
# print(dev_001_list)
        # if pvc['metadata']['name'] in data['metadata']['name']:
        #     print(pvc['metadata']['name'])
            
# with open('new-pvc.yaml', 'r') as file:
#     new_config = yaml.safe_load_all(file)
#     print(list(new_config))

# combine_list = dev_001_list + pvc_001_list
# print(combine_list)