# The script returns a kubeconfig for the service account given
# you need to have kubectl on PATH with the context set to the cluster you want to create the config for

# Change these variables according to your projects - clusterName, server & namespace and execute it
clusterName=onyx
# your server address goes here get it via `kubectl cluster-info`
server=https://<>ip-address>:6443
# the Namespace and ServiceAccount name that is used for the config
namespace=default

serviceAccount=default-editor
secretName='default-editor-token'

######################
# actual script starts
set -o errexit


ca=$(kubectl --namespace $namespace get secret/$secretName -o jsonpath='{.data.ca\.crt}')
token=$(kubectl --namespace $namespace get secret/$secretName -o jsonpath='{.data.token}' | base64 --decode)

echo "
---
apiVersion: v1
kind: Config
clusters:
  - name: ${clusterName}
    cluster:
      certificate-authority-data: ${ca}
      server: ${server}
contexts:
  - name: ${serviceAccount}@${clusterName}
    context:
      cluster: ${clusterName}
      namespace: ${namespace}
      user: ${serviceAccount}
users:
  - name: ${serviceAccount}
    user:
      token: ${token}
current-context: ${serviceAccount}@${clusterName}
"
