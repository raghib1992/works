from kubernetes import client, config
import argparse
import csv
import datetime
from datetime import timezone

# Get the detial of notebook pod
def notebook_details(namespace):

    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()
    
    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(
            namespace=namespace,
            label_selector='notebook-name'
        )
        pod_name = []
        for pod in pods.items:
            pod_name.append(pod.metadata.name)
    except Exception as e:
        print(f"Error listing pods: {e}")
        return []
            
    try:
        pod_detials = []
        for pod in pod_name:
            pod_list = {}
            pod_detail = v1.read_namespaced_pod(name=pod, namespace=namespace)
            # print(pod_detail)
            pod_list['NotebookName'] = pod_detail.metadata.owner_references[0].name
            pod_list['NotebookImageName'] = pod_detail.spec.containers[0].image
            pod_list['NotebookCpuRequest'] = pod_detail.spec.containers[0].resources.requests["cpu"]
            pod_list['NotebookMemoryRequest'] = pod_detail.spec.containers[0].resources.requests['memory']
            pod_list['IsNotebookGpu'] = bool([device for device in pod_detail.spec.containers[0].resources.requests if device.startswith("nvidia")])
            pod_list['NotebookVolumeClaimName'] = [vol.persistent_volume_claim.claim_name for vol in pod_detail.spec.volumes if vol.persistent_volume_claim != None][0]
            time = str(datetime.datetime.now(timezone.utc) - pod_detail.metadata.creation_timestamp)
            # print(time.split(":"))
            pod_list['NotebookPodStartPeriod'] = f"{time.split(":")[0]} Hours and {time.split(":")[1]} minutes"
            pod_detials.append(pod_list)
    except Exception as e:
        print(f"Error retrieving pod information: {e}")
        return {}

    # print(pod_detials)
    return pod_detials

# Create csv file of details of Notebook
def create_csv(notebook):
    notebook_detail = notebook
    fields = ['NotebookName', 'NotebookImageName', 'NotebookCpuRequest', 'NotebookMemoryRequest', 'IsNotebookGpu', 'NotebookVolumeClaimName', 'NotebookPodStartPeriod'] 

    with open('notebook_details.csv', 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(notebook_detail)

parser = argparse.ArgumentParser(description="Passing Variable from command line")
parser.add_argument("-n", "--namespace", help="namespace")
args = parser.parse_args()
args = vars(args)
namespace = args["namespace"]

# Need to pass namespace as arguments when run this python script
notebook = notebook_details(namespace)
create_csv(notebook)
