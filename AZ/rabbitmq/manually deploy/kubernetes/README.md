### Install rabbitmq cluster-operator
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml

### Install rabbitmq cluster
```
apiVersion: rabbitmq.com/v1beta1
kind: RabbitmqCluster
metadata:
  name: myrabbit
spec:
  replicas: 3
  image: rabbitmq:3.9-management
  rabbitmq:
    additionalPlugins:
    - rabbitmq_stream
```

### Check pods
kubectl get pods

### Install krew
##### https://krew.sigs.k8s.io/docs/user-guide/setup/install/

### Install kubectl rabbitmq plugin
kubectl krew install rabbitmq

