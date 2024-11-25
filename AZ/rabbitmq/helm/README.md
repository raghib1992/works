1. Using terragrunt hcl file created application in argocd using helm 
2. bitnami helm chart used to deploy rabbitmq-operator and rabbitmq
3. 
















NOTE: It is mandatory to specify the password and Erlang cookie that was set the first time the chart was installed when upgrading the chart. Otherwise, new pods won't be able to join the cluster.
https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq#horizontal-scaling


The RabbitMQ quorum queue is a modern queue type which implements a durable, replicated queue based on the Raft consensus algorithm and should be considered the default choice when needing a replicated, highly available queue.


https://stackoverflow.com/questions/66715405/how-to-auto-scale-helm-chart-rabbitmq-statefulset