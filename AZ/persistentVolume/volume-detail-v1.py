import kubernetes
from kubernetes import client, config
import csv 
import argparse
import os

parser = argparse.ArgumentParser(description="Cluster name")
parser.add_argument("-c", "--clusterName", help="cluster_name")
parser.add_argument("-p", "--prid", help="prid")
parser.add_argument("-n", "--namespace", help="namespace")
args = parser.parse_args()
args = vars(args)
cluster = args["clusterName"]
prid = args["prid"]
namespace = args["namespace"]

if cluster == 'dev':
    config.load_kube_config(config_file=os.environ['KUBECONFIG'],context='ai-ops-brown@kubernetes')
else:
    config.load_kube_config(config_file=os.environ['KUBECONFIG'],context=f"ai-ops-{cluster}@kubernetes")

# config.load_kube_config()

core_v1 = client.CoreV1Api()
pvc = core_v1.list_persistent_volume_claim_for_all_namespaces()
# print(pvc)


pvc_list = []
for item in pvc.items:
    # pvc_details = {}
    ns = item.metadata.namespace
    pvc_name = item.metadata.name
    sort_pvc_name = pvc_name.split("-")[0]
    
    if sort_pvc_name == prid and namespace == ns:
        pvc_list.append(item.metadata.name)
# print(pvc_list)  
      
fields = ["PVC_Name", "PV_Name", "Namespace"]
with open("volume_details.csv", 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(pvc_list)