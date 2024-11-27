1. Using terragrunt hcl file created application in argocd using helm

2. bitnami helm chart used to deploy rabbitmq-operator and rabbitmq

3. It is mandatory to specify the password and Erlang cookie that was set the first time the chart was installed when upgrading the chart. Otherwise, new pods won't be able to join the cluster.

4. [bitnami_horizontal_scaling](https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq#horizontal-scaling)


4. The RabbitMQ quorum queue is a modern queue type which implements a durable, replicated queue based on the Raft consensus algorithm and should be considered the default choice when needing a replicated, highly available queue.

Ref:
 - [RabbitMQ_scaleout_issue](https://stackoverflow.com/questions/66715405/how-to-auto-scale-helm-chart-rabbitmq-statefulset)

- [RammitMQ-HPA](https://ryanbaker.io/2019-10-07-scaling-rabbitmq-on-k8s/)
