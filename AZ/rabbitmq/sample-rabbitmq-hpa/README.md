### Create namespace
kubectl create ns rabbit

### Install rabbitmq-operator
helm install rabbitmq-opertor bitnami/rabbitmq-cluster-operator -n rabbit

### Install rabbitmq
helm install rabbitmq bitnami/rabbitmq -n rabbit -f rabbit-values.yaml

### Install Prometheus
helm install prometheus prometheus-community/prometheus -n rabbit

### Install Prometheus-Adapter
helm install prometheus-adapter prometheus-community/prometheus-adapter -n rabbit

helm upgrade prometheus-adapter prometheus-community/prometheus-adapter -n rabbit -f config.yaml


### Ceate app
create docker file
create image
create chart
helm install rabbitmq-sample-app ./Charts/rabbitmq-sample-app -n rabbit

### Uninstall
helm uninstall rabbitmq-sample-app -n rabbit
helm uninstall prometheus-adapter -n rabbit
helm uninstall prometheus -n rabbit
helm uninstall rabbitmq-opertor -n rabbit
helm uninstall rabbitmq -n rabbit
