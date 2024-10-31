# Installation
### Install using helm
- Add repo
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm show values bitnami/rabbitmq
```


# Reference
- *https://github.com/rabbitmq/cluster-operator*

OK40b5XTAWupFe3a
hE2HJbIKVfOxNSIs

rabbitmqImage = {
    registry = "harbor.csis.astrazeneca.net"
    repository = "bitnami/rabbitmq"
    tag = "4.0.2-debian-12-r0"
}
msgTopologyOperator = {
    image = {
    registry = "harbor.csis.astrazeneca.net"
    repository = "bitnami/rmq-messaging-topology-operator"
    tag = "1.15.0-debian-12-r0"
    }
}
clusterOperator ={ 
    image = {
    registry = "harbor.csis.astrazeneca.net"
    repository = "bitnami/rabbitmq-cluster-operator"
    tag = "2.11.0-debian-12-r0"
    }
}
credentialUpdaterImage ={ 
    image = {
    registry = "harbor.csis.astrazeneca.net"
    repository = "bitnami/rmq-default-credential-updater"
    tag = "1.0.4-debian-12-r29"
    }
}