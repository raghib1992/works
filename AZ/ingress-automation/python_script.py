from jinja2 import Environment, FileSystemLoader
import yaml
import argparse
import os

def get_file_name(cluster,namespace):
    if cluster == 'dev':
        sort_namespace = "-".join(namespace.split("-")[-2:])
        file_name = f"{sort_namespace}.yaml"
    elif cluster in ['iron', 'bronze', 'lead' ]:
        sort_name = namespace.split('-')
        if cluster not in sort_name:
            file_name = f"{namespace}.yaml"
        else:
            sort_namespace = "-".join(sort_name[-2:])
            file_name = f"{sort_namespace}.yaml"
    else:
      file_name = f"{namespace}.yaml"
    if not os.path.exists(f"../states/{cluster}/{file_name}"):
        with open(f"../states/{cluster}/{file_name}", "w") as file:
            file.write("")
    print(f"file_name in namespace {namespace} is {file_name}")
    return file_name

def check_new_line(cluster,filename):
    file = f"../states/{cluster}/{filename}"
    with open(file, 'rb+') as f:
        f.seek(-1, 2)
        last_byte = f.read(1)
        if last_byte == b'-':
            f.write(b'\n')
        elif last_byte == b'\n':
            f.seek(-2,2)
            second_line=f.read(1)
            if second_line == b'-':
                pass
            else:
                f.write(b'\n---\n')
        else:
            f.write(b'\n---\n')

def create_ingress_manifest(*args):
    env = Environment(loader=FileSystemLoader('../templates'))
    template = env.get_template('ingress_template.yaml.j2')
    rendered_yaml = template.render(
        NAME = name,
        NAMESPACE = namespace,
        HOST = host,
        SERVICE = service,
        PORT = port
    )
    return rendered_yaml

def merge_ingress(cluster,file_name,ingress_manifest):
    filename = f"../states/{cluster}/{file_name}"
    with open(filename, 'a') as f:
        f.write(ingress_manifest)
        print(f"YAML file '{filename}' created successfully.")
        
parser = argparse.ArgumentParser(description="required values for Ingress manifest file")
parser.add_argument("-c", "--clusterName", help="cluster_name")
parser.add_argument("-a", "--namespace", help="namespace")
parser.add_argument("-n", "--name", help="ingress_name")
parser.add_argument("-s", "--service", help="service_name")
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-r", "--host", help="host")
args = parser.parse_args()
args = vars(args)
cluster = args["clusterName"]
namespace = args["namespace"]
name = args["name"]
service = args["service"]
port = args["port"]
host = args["host"]

filename = get_file_name(cluster, namespace)
check_new_line(cluster,filename)
ingress_manifest = create_ingress_manifest(name,namespace,host,service,port)
merge_ingress(cluster,filename,ingress_manifest)
check_new_line(cluster,filename)

# python generate_ingress_manifest.py -c dev -a brown-dev-005 -n ingress-test -s test-service -p 80 -h test.paas-brown.as.com