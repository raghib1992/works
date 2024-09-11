# import yaml
# from kubernetes import client, config

# config.load_kube_config()
# core_v1 = client.CoreV1Api()



# def get_profile(cluster):
#     api_instance = client.CustomObjectsApi()
#     profiles = api_instance.list_cluster_custom_object(group="kubeflow.org",version="v1",plural="profiles")
#     namespace = [profile['metadata']['name'] for profile in profiles.get('items', [])]
#     return namespace
    
# cluster = 'bronze'    
# # profile = get_profile(cluster)
# profile = ['active-learning-biologics', 'adapt', 'afe', 'alxn-it-ai-poc', 'andexxa', 'axial-data-profiling', 'az-ceeba-analyses-and-predictions', 'az-cp-launch', 'azal', 'bco-ai-projects', 'bdp-design', 'bronze-dev-001', 'crystal-segmentation-dev', 'crystal-segmentation-prod', 'dev-afe', 'dev-enterprise-graph', 'deviation-similarity', 'dna-z-dev', 'dna-z-preprod', 'dna-z-prod', 'drc-minutes-query-tool', 'eais-computer-vision', 'eais-line-clearance', 'enterprise-mlops', 'erv-rag', 'euit-ai-projects', 'finance', 'gbs-analytics', 'gen-ai-poc-qr-and-tw', 'genaipot-r2r-bsr', 'gpt-procurement-contracting', 'office-attendance', 'pqs', 'predictino', 'prod-afe', 'prod-axial-data-profiling', 'ptd-digital-twin', 'quest', 'quest-ppt', 'quest-prod', 'resonance', 'sandworm', 'sandworm-dev', 'sandworm-qa', 'shawcad', 'sweops-maintenance-bot', 'test-afe']
# # print(profile)

# # profile = ['brown-dev-001']

# if cluster == 'dev':
#     for namespace in profile:
#         sort_namespace = "-".join(namespace.split("-")[-2:])
#         filename = f"{sort_namespace}.yaml"
#         print(filename)
# elif cluster in ['iron', 'bronze', 'lead' ]:
#     for namespace in profile:
#         sort_name = namespace.split('-')
#         # print(sort_name)
#         if cluster not in sort_name:
#             filename = f"{namespace}.yaml"
#         else:
#             # print(sort_name)
#             sort_namespace = "-".join(sort_name[-2:])
#             filename = f"{sort_namespace}.yaml"
#             print(filename)
# else:
#     for namespace in profile:
#         file_name = f"{namespace}.yaml"
#     # if len(sort_namespace) >= 2:
#     #     sort_namespace = sort_namespace[-2]


    # print(sort_namespace)
    # if sort_namespace == 'dev':
    #     filename = cluster-sort_names
from jinja2 import Environment, FileSystemLoader
import yaml
import argparse
import os
cluster = 'onyx'
file_name = f"manifest.yaml"
def existing_pv_detial(cluster,file_name):
    # filename = f"../states/{cluster}/{file_name}"
    # print(filename)
    with open(file_name, 'r') as file:
        file_list = list(yaml.safe_load_all(file))
        for data in file_list:
            if data is not None:
                print(data)
                print('----------------------------------')
    
    
existing_pv_detial(cluster,file_name)