# Ollama
Ollama is an open-source platform that simplifies running and customizing large language models (LLMs) locally.


# Understanding Ollama’s Model Storage
Let’s start by understanding how Ollama handles model storage. By default, Ollama saves its models in the ~/.ollama/models directory, which contains both model blobs and manifests.

1. **Model blobs** are large binary objects that store the actual parameters and data of a machine learning model, essential for making predictions or further training.
2. **Manifests** provide metadata and information about a machine learning model, including its architecture, hyperparameters, and version information, facilitating model selection and integration into production systems.










Create DB

Create open-webui app

Create ollama

Create ubuntu pod to exec into db
```t
kubectl -n open-webui exec -ti ubuntu -- /bin/bash
cd /usr/local/lib/python3.11/site-packages

# Connect to db
psql -h open-webui-cnpg-db-rw -U app -d app;
```

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
