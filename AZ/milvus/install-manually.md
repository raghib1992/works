kubectl get pods -n cert-manager

helm install milvus-operator -n milvus-operator --create-namespace --wait --wait-for-jobs https://github.com/zilliztech/milvus-operator/releases/download/v1.1.1/milvus-operator-1.1.1.tgz
