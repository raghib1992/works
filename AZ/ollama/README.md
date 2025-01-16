# Ollama
Ollama is an open-source platform that simplifies running and customizing large language models (LLMs) locally.


## Understanding Ollama’s Model Storage
Let’s start by understanding how Ollama handles model storage. By default, Ollama saves its models in the **~/.ollama/models** directory, which contains both model blobs and manifests.

1. **Model blobs** are large binary objects that store the actual parameters and data of a machine learning model, essential for making predictions or further training.
2. **Manifests** provide metadata and information about a machine learning model, including its architecture, hyperparameters, and version information, facilitating model selection and integration into production systems.

# Open-webUI
Open WebUI is a Web-based interface that allows you to interact with AI models, such as large language models (LLMs). It simplifies working with AI by providing a graphical user interface (GUI)


# Create ollama
#### manifest file
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ollama
  namespace: open-webui
spec:
  selector:
    matchLabels:
      app: ollama
  serviceName: "ollama"
  template:
    spec:
      containers:
      - name: ollama
        env:
          - name: http_proxy
            value: http://azpse.astrazeneca.net:9480
          - name: https_proxy
            value: http://azpse.astrazeneca.net:9480
          - name: no_proxy
            value: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
        resources:
          limits:
            cpu: '27'
            memory: 110Gi
            nvidia.com/gpu: '2'
          requests:
            cpu: '27'
            memory: 110Gi
      nodeSelector:
        accelerator: A100-SXM4-40GB
      tolerations:
        - key: "GPU_workload"
          operator: "Equal"
          value: "true"
          effect: "NoSchedule"
```
# Create Open-webui
#### open-webui manifest file
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: open-webui-deployment
  namespace: open-webui
spec:
  template:
    spec:
      containers:
      - name: open-webui
        env:
          - name: OLLAMA_BASE_URL
            value: "http://ollama-service.open-webui.svc.cluster.local:11434"
          - name: ENABLE_OAUTH_SIGNUP
            value: "true"
          - name: WEBUI_URL
            value: "https://azimuth-chatgpt.paas-onyx.astrazeneca.net"
          - name: OPENID_REDIRECT_URI
            value: "https://azimuth-chatgpt.paas-onyx.astrazeneca.net/oauth/oidc/callback"
          - name: DEFAULT_USER_ROLE
            value: "user"
          - name: ENABLE_SIGNUP
            value: "true"
          - name: RAG_EMBEDDING_ENGINE
            value: "ollama"
          - name: WEBUI_NAME
            value: "Azimuth"
          - name: OLLAMA_HOME
            value: "/app/backend/data/.ollama"
          # - name: http_proxy
          #   value: http://azpse.astrazeneca.net:9480
          # - name: https_proxy
          #   value: http://azpse.astrazeneca.net:9480
          # - name: no_proxy
          #   value: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
        resources:
          limits:
            cpu: 8000m
            memory: 16Gi
          requests:
            cpu: 4000m
            memory: 8Gi
        envFrom:
          - secretRef:
              name: ollama-secret
        tty: true
        volumeMounts:
        - name: webui-volume
          mountPath: /app/backend/data
      volumes:
      - name: webui-volume
        persistentVolumeClaim:
          claimName: open-webui-pvc 

```
#### pvc manifest file
```yml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    app: open-webui
  name: open-webui-pvc
  namespace: open-webui
spec:
  accessModes: ["ReadWriteMany"]
  storageClassName: "ontap-silver"
  resources:
    requests:
      storage: 500Gi
```
#### secret
```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: ollama-secret
  namespace: open-webui
  annotations:
    avp.kubernetes.io/path: "aiops/data/dev/ollama"
stringData:
# Secret store in vault, and argo cd has plugin to pull it and apply
  OAUTH_CLIENT_ID: <microsoft_client_id>
  OAUTH_CLIENT_SECRET: <microsoft_client_secret>
  OPENID_PROVIDER_URL: <microsoft_endpoint>
  DATABASE_URL: <database_url>
```
#### Kustomization file
```yaml
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - https://github.com/open-webui/open-webui.git/kubernetes/manifest/base?ref=v0.4.8
  - secret.yaml
  - base/webui-cnpg.yaml
  # - base/open-webui.yaml
  # - base/webui-secret.yaml
  # - base/webui-deployment.yaml
  # - base/webui-service.yaml
  # - base/webui-ingress.yaml
  # - base/webui-pvc.yaml

patchesStrategicMerge:
  - ollama-statefulset-gpu.yaml
  - ingress.yaml
  - webui-deployment.yaml
  - webui-pvc.yaml

images:
  - name: ollama/ollama:latest
    newName: harbor.csis.astrazeneca.net/ollama/ollama
    newTag: 0.5.4
  - name: ghcr.io/open-webui/open-webui:main
    newName: harbor.csis.astrazeneca.net/ghcr.io/open-webui/open-webui
    newTag: v0.5.3
```
# Create cnpg db
```yml
apiVersion: v1
data:
  username: YXBw
  password: dzRZMEVPaGdqcU1ROFc=
kind: Secret
metadata:
  name: app-secret
  namespace: open-webui
  labels:
    cnpg.io/reload: ""
type: kubernetes.io/basic-auth
---
apiVersion: v1
data:
  username: cG9zdGdyZXM=
  password: YnBScUVNbmdzYUpLZEw=
kind: Secret
metadata:
  name: superuser-secret
  namespace: open-webui
  labels:
    cnpg.io/reload: ""
type: kubernetes.io/basic-auth
---
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: open-webui-cnpg-db
  namespace: open-webui
spec:
  instances: 1 # This will create one primary instance,two replica instances
  
  enableSuperuserAccess: true
  superuserSecret:
    name: superuser-secret
  # unsupervised: automated update of the primary once all replicas have been upgraded (default)
  primaryUpdateStrategy: unsupervised
  postgresql:
    parameters:
      log_statement: "ddl"
      log_checkpoints: "on"
      max_slot_wal_keep_size: "10GB"
  imageName: harbor.csis.astrazeneca.net/azimuth-images/postgresql:16.4
  imagePullPolicy: Always
  # Environment variables for proxy settings
  env:
  - name: http_proxy
    value: http://azpse.astrazeneca.net:9480
  - name: https_proxy
    value: http://azpse.astrazeneca.net:9480
  - name: no_proxy
    value: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
  # Persistent storage configuration
  storage:
    storageClass: ontap-silver
    size: 1Gi
  # Backup properties
  backup:
    barmanObjectStore:
      destinationPath: s3://az-eu-azimuth-kfp-dev/artifacts/onyx-dev-001/pg
      endpointURL: https://s3.eu-west-1.amazonaws.com
      s3Credentials:
        accessKeyId:
          name: mlpipeline-minio-artifact
          key: accesskey
        secretAccessKey:
          name: mlpipeline-minio-artifact
          key: secretkey
      wal:
        compression: gzip
        maxParallel: 8
        encryption: AES256
      data:
        compression: gzip
        encryption: AES256
    retentionPolicy: "30d"
  walStorage:
    size: 2Gi
  bootstrap:
    initdb:
      database: app
      owner: app
      secret:
        name: app-secret
      postInitTemplateSQL:
        - CREATE EXTENSION vectorscale CASCADE;
        - CREATE EXTENSION age;
        - ALTER USER app WITH SUPERUSER;

  resources:
    requests:
      memory: "0.5Gi"
      cpu: "1"
    limits:
      memory: "0.5Gi"
      cpu: "1"
```

# Create ubuntu pod to exec into db
#### manifest file
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-limited-deployment
  namespace: open-webui
spec:
  replicas: 1 # Number of Pod replicas
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: harbor.csis.astrazeneca.net/azimuth-demo/cpu-codeserver:latest
        ports:
        - containerPort: 80
        resources:
          requests: # Minimum resources required
            cpu: 1 # 200 millicores (0.5 CPU core)
            memory: 1Gi # 500 mebibytes
          limits: # Maximum resources allowed
            cpu: 1 # 500 millicores (0.5 CPU core)
            memory: 1Gi # 512 mebibytes
```
- Verify cluster
```sh
kubectl get clusters
    # STATUS should be "Cluster in healthy state"
kubectl get pods
    # 3 pods should get created for this cluster
kubectl get svc
    #open-webui-cnpg-db-rw service should be running
```
- Exec into pod
```sh
kubectl -n open-webui exec -ti resource-limited-deployment-55965798cd-m56sr -- /bin/bash
```
- Get password
```sh
kubectl get secret app-secret -o=jsonpath='{.data.password}' | base64 -d
# w4Y0EOhgjqMQ8W
```
- Connect to db
```sh
psql -h open-webui-cnpg-db-rw -U app -d app;
```
- check tables
```
\dt

\dt+

# Show tables in all databases
\dt *
```
- Check databases
```
\l
```
- Get tables data
```t
SELECT * FROM tables_name;
SELECT * FROM model;

# show number of rows in tables
SELECT COUNT(*) FROM chat;

# Limit ot row one
SELECT * FROM model limit 1;
```
## Dump table data to local
```t
# dump file from database to pod
psql -d database_name -c "\copy table_name TO 'file.json'" database_name
psql -d app -c "\copy chat TO 'chat.json'" app
psql -h open-webui-cnpg-db-rw -U app -d app -c "\copy chat TO 'chat.json'" app
```

## Copying Files from Pod to Local Machine in Kubernetes
```
kubectl cp <pod_name>:<path_to_file> /local/path/
kubectl -n open-webui cp resource-limited-deployment-55965798cd-m56sr:/app/chat.json ./chat.json
```
**********

# exec into ollama pod
```sh
kubectl -n open-webui exec -ti ollama-0 -- /bin/bash
```

### check module and chat
```t
# go to root folder
cd
# check files
ls -la
# go to .ollama folder
cd .ollama
# sha files
cd models/blobs
# module manifest
cd .ollama/models/manifests/registry.ollama.ai/library
```
