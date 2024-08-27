# Link https://k8s-python.readthedocs.io/en/stable/genindex.html

from kubernetes import client, config
import argparse
import csv
import datetime
from datetime import timezone

def kubernetes_auth():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()
    return

# Get list of Profiles
def namespace_list(auth):
    api_instance = client.CustomObjectsApi()
    profiles = api_instance.list_cluster_custom_object(group="kubeflow.org",version="v1",plural="profiles")
    namespace = [profile['metadata']['name'] for profile in profiles.get('items', [])]
    return namespace

# Get the detial of notebook pod
def notebook_details(auth, namespace, cluster_name):   
    api_v1 = client.CoreV1Api()
    api_instance = client.CustomObjectsApi()
    pod_details = []
    for ns in namespace:
        pods = api_v1.list_namespaced_pod(namespace=ns,label_selector='notebook-name')
        pod_name = [ pod.metadata.name for pod in pods.items ]      
        try:
            pvc_list = api_v1.list_namespaced_persistent_volume_claim(namespace=ns)
            for pod in pod_name:
                pod_list = {}
                pod_detail = api_v1.read_namespaced_pod(name=pod, namespace=ns)
                notebook_name = pod_detail.metadata.owner_references[0].name
                pod_list['NotebookName'] = notebook_name
                pod_list['ClusterName'] = cluster_name
                pod_list['Namespace'] = ns
                pod_list['PodName'] = pod
                pod_list['NotebookImageName'] = pod_detail.spec.containers[0].image
                pod_list['NotebookCpuRequest'] = pod_detail.spec.containers[0].resources.requests["cpu"]
                pod_list['NotebookMemoryRequest'] = pod_detail.spec.containers[0].resources.requests['memory']
                pod_list['IsNotebookGpu'] = bool([device for device in pod_detail.spec.containers[0].resources.requests if device.startswith("nvidia")])
                claimName = [vol.persistent_volume_claim.claim_name for vol in pod_detail.spec.volumes if vol.persistent_volume_claim != None][0]
                pod_list['NotebookVolumeClaimName'] = claimName
                time = str(datetime.datetime.now(timezone.utc) - pod_detail.metadata.creation_timestamp)
                pod_list['NotebookPodStartPeriod'] = f"{time.split(":")[0]} Hours and {time.split(":")[1]} minutes"
                notebooks = api_instance.list_namespaced_custom_object(group="kubeflow.org",version="v1",namespace=ns,plural="notebooks")
                pod_list['NotebookCreator'] = [item['metadata']['annotations']['notebooks.kubeflow.org/creator'] for item in notebooks['items'] if notebook_name in item['metadata']['name']][0]
                pod_list['NotebookGpu'] =  pod_detail.spec.containers[0].resources.requests['nvidia.com/gpu'] if 'nvidia.com/gpu' in pod_detail.spec.containers[0].resources.requests else None
                pod_list['NotebookClaimCapacity'] = [item.spec.resources.requests['storage'] for item in pvc_list.items if claimName in item.metadata.name][0]
                pod_details.append(pod_list)
        except Exception as e:
            print(f"Error retrieving pod information: {e}")
            return {}
    
    return pod_details

# Create csv file of details of Notebook
def create_csv(notebook):
    notebook_detail = notebook
    fields = ['ClusterName', 'Namespace','NotebookName', 'PodName','NotebookImageName', 'NotebookCpuRequest', 'NotebookMemoryRequest', 'IsNotebookGpu', 'NotebookGpu', 'NotebookVolumeClaimName', 'NotebookClaimCapacity', 'NotebookPodStartPeriod', 'NotebookCreator'] 

    with open('notebook_details.csv', 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(notebook_detail)

parser = argparse.ArgumentParser(description="Passing Variable from command line")
parser.add_argument("-c", "--clusterName", help="namespace")
args = parser.parse_args()
args = vars(args)
cluster_name = args["clusterName"]

# Need to pass cluster name as arguments when run this python script
auth = kubernetes_auth()
namespace = namespace_list(auth)
notebook = notebook_details(auth, namespace, cluster_name)
create_csv(notebook)
