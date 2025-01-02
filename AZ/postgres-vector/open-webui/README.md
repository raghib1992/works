
Create DB

Create open-webui app

Create ubuntu pod to exec into db
```
kubectl -n open-webui exec -ti ubuntu -- /bin/bash
cd /usr/local/lib/python3.11/site-packages

# Connect to db
psql -h open-webui-cnpg-db-rw -U app -d app;
```


write /root/.ollama/models/blobs/sha256-28bfdfaeba9f51611c00ed322ba684ce6db076756dbc46643f98a8a748c5199e-partial: no space left on device