Created by Nadim, MdRaghib (LTIMindtree), last modified just a moment ago, viewed 5 times
Introduction
RabbitMQ is a message-queueing software also known as a message broker or queue manager. Simply said; it is software where queues are defined, to which applications connect in order to transfer a message or messages.

A message broker acts as a middleman for various services (e.g. a web application). They can be used to reduce loads and delivery times of web application servers by delegating tasks that would normally take up a lot of time or resources to a third party that has no other job. The basic architecture of a message queue is simple - there are client applications called producers that create messages and deliver them to the broker (the message queue). Other applications, called consumers, connect to the queue and subscribe to the messages to be processed. Software may act as a producer, or consumer, or both a consumer and a producer of messages. Messages placed onto the queue are stored until the consumer retrieves them.

RabbitMQ and server concepts
Some important concepts need to be described before we dig deeper into RabbitMQ. The default virtual host, the default user, and the default permissions are used in the examples, so let’s go over the elements and concepts:

Producer: Application that sends the messages.
Consumer: Application that receives the messages.
Queue: Buffer that stores messages.
Message: Information that is sent from the producer to a consumer through RabbitMQ.
Connection: A TCP connection between your application and the RabbitMQ broker.
Channel: A virtual connection inside a connection. When publishing or consuming messages from a queue - it's all done over a channel.
Exchange: Receives messages from producers and pushes them to queues depending on rules defined by the exchange type. To receive messages, a queue needs to be bound to at least one exchange.
Binding: A binding is a link between a queue and an exchange.
Routing key: A key that the exchange looks at to decide how to route the message to queues. Think of the routing key like an address for the message.
AMQP: Advanced Message Queuing Protocol is the protocol used by RabbitMQ for messaging.
Users: It is possible to connect to RabbitMQ with a given username and password. Every user can be assigned permissions such as rights to read, write and configure privileges within the instance. Users can also be assigned permissions for specific virtual hosts.
Vhost, virtual host: Provides a way to segregate applications using the same RabbitMQ instance. Different users can have different permissions to different vhost and queues and exchanges can be created, so they only exist in one vhost.
Setup RabbitMQ Cluster
There are various way to install RabbitMQ. 

We deploy RabbitMQ Cluster Operator in a Kubernetes using helm.

Step 1: Need to Add Bitnami Repo in azimuth-deployment/argocd-project-configuration/terragrunt.hcl 
```
external_repos = {
      rabbitmq-cluster-operator = {
      url  = "https://charts.bitnami.com/bitnami"
      type = "helm"
      name = "rabbitmq-cluster-operator"
    }
}
```

Step 2: Create HCL file in azimuth-deployment repo. Details of code to create application is below.

Step 3: Deploy RabbitMQ Cluster Operator in ArgoCD
```
app_name = {
    rabbitmq-operator-nonlive = {
      priority        = "0"
      repo_url        = "https://charts.bitnami.com/bitnami"
      enable_replace  = true
      target_revision = "4.3.25"
      path            = "rabbitmq-cluster-operator"
      namespace       = "rabbitmq-system"
      clusters        = local.clusters
      plugin_name     = "argocd-vault-plugin-helm"
      helm_args       = "--namespace rabbitmq-system --include-crds"
      helm_values     = {
        global = {
          imageRegistry = "harbor.csis.astrazeneca.net"
        }
      }
    }
}
```

Step 4: Create RabbitMQ Instance in ArgoCD
```
rabbitmq-cluster-nonlive = {
      priority        = "1"
      repo_url        = "https://charts.bitnami.com/bitnami"
      enable_replace  = true
      target_revision = "15.0.4"
      path            = "rabbitmq"
      namespace       = "rabbitmq-system"
      clusters        = local.clusters
      plugin_name     = "argocd-vault-plugin-helm"
      helm_args       = "--namespace rabbitmq-system --include-crds"
      helm_values     = {
        global = {
          imageRegistry = "harbor.csis.astrazeneca.net"
        }
        replicaCount  = 1
        service = {
          type        = "ClusterIP"
        }
        metrics = {
          enabled = true
        }
        ingress = {
          enabled     = true
          path        = "/"
          pathType    = "Prefix"
          hostname    = "rabbitmq.paas-brown.astrazeneca.net"
          ingressClassName = "nginx"
          annotations = {
            "nginx.ingress.kubernetes.io/proxy-body-size"     = "2000M"
            "nginx.ingress.kubernetes.io/proxy-read-timeout"   = "180"
            "nginx.ingress.kubernetes.io/proxy-send-timeout"  = "180"
          }
        }
        auth = {
          username = "rabbit"
          password = "<path:aiops/data/dev/rabbitmq#password>" #Hashicorp-vault plugin install in argocd, it will pull secret from the mention path
        }
        configuration = <<EOF
## Username and password
default_user = {{ .Values.auth.username }}
{{- if and (not .Values.auth.securePassword) .Values.auth.password }}
default_pass = {{ .Values.auth.password }}
{{- end }}
EOF
      }
    }
```

Step 5: Test Hello World example using Python Script

Send message to RabbitMQ queue
send.py
```
#!/usr/bin/env python
import pika
 
 
rabbitmq_host = 'dev-azimuth-rabbitmq-cluster-nonlive-0.dev-azimuth-rabbitmq-cluster-nonlive-headless.rabbitmq-system.svc.cluster.local'
rabbitmq_port = 5672
rabbitmq_user = 'test'
# To get the the password- get from secret - dev-azimuth-rabbitmq-cluster-nonlive
rabbitmq_password = 'test123'
 
 
# Create a credentials object
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
 
# Define connection parameters
connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials,
    virtual_host='brown-dev-001'
)
 
# Establish connection to RabbitMQ
try:
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
     
    print("Connected to RabbitMQ successfully!")
     
    # Example of creating a queue
    channel.queue_declare(queue='hello')
 
    countries_and_code = {
        'CANADA': 'CA',
        'FRANCE': 'FR',
        'GERMANY': 'DE',
        'GREECE': 'GR',
        'HONG KONG': 'HK',
        'ICELAND': 'IS',
        'INDIA': 'IN',
        'INDONESIA': 'ID',
        'IRAN, ISLAMIC REPUBLIC OF': 'IR',
        'JAPAN': 'JP',
        'KUWAIT': 'KW',
        'LUXEMBOURG': 'LU',
        'MADAGASCAR': 'MG',
        'MALDIVES': 'MV',
        'MAURITIUS': 'MU',
        'NEPAL': 'NP',
        'NEW ZEALAND': 'NZ',
        'QATAR': 'QA',
        'SAUDI ARABIA': 'SA',
        'SWITZERLAND': 'CH',
        'TURKEY': 'TR',
        'UNITED ARAB EMIRATES': 'AE',
        'UNITED KINGDOM': 'GB',
        'UNITED STATES': 'US'
    }
 
    for country in countries_and_code:
        channel.basic_publish(exchange='', routing_key='hello', body=f"Hello {country}",properties=pika.BasicProperties(delivery_mode=2,))
        print(f" [x] Sent 'Hello {country}!'")
     
    # Close the connection
    connection.close()
    print("Connection closed.")
     
except Exception as e:
    print(f"Failed to connect to RabbitMQ: {e}")
```

receive.py
```
#!/usr/bin/env python
import pika, sys, os
 
rabbitmq_host = 'dev-azimuth-rabbitmq-cluster-nonlive-0.dev-azimuth-rabbitmq-cluster-nonlive-headless.rabbitmq-system.svc.cluster.local'
rabbitmq_port = 5672
rabbitmq_user = 'test'
# To get the the password- get from secret - dev-azimuth-rabbitmq-cluster-nonlive
rabbitmq_password = 'test123'
 
def main():
    # Create a credentials object
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
 
    # Define connection parameters
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=credentials
        virtual_host='brown-dev-001'
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
 
    channel.queue_declare(queue='hello')
 
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
 
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
 
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
```

Create User
Create User using Web-UI
Create vhost: 
In a single-tenant environment, for example, when your RabbitMQ cluster is dedicated to power a single system in production, using default virtual host (/) is perfectly fine.

In multi-tenant environments, use a separate vhost for each tenant/environment, e.g. project1_development, project1_production, project2_development, project2_production, and so on

Click on Admin tab


b. Click on Virtual Host on Right side 

c. Fill the tab for Name, Description and Tag



d. Click on Add Virtual Host



2. Create User



a. Click on User in Right side panel

b. Fill the all tabs for Add user

c. Click on button for Add User



3. Give Access to User

a. Click on username (here click on bob)



b. In Set Permission BLock, select virtual host, and fill regexp as per permission you want want to five to user. "*" for all permission




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