Unable to delete application: error patching application with finalizers: Application.argoproj.io "onyx-azimuth-milvus-core-nonlive" is invalid: metadata.finalizers: Forbidden: no new finalizers can be added if the object is being deleted, found new finalizers []string{"resources-finalizer.argocd.argoproj.io/foreground"}
Unable to delete application: error patching application with finalizers: Application.argoproj.io "onyx-azimuth-milvus-core-nonlive" is invalid: metadata.finalizers: Forbidden: no new finalizers can be added if the object is being deleted, found new finalizers []string{"resources-finalizer.argocd.argoproj.io/foreground"}


kubectl patch some-resource/some-name \
    --type json \
    --patch='[ { "op": "remove", "path": "/metadata/finalizers" } ]'

kubectl --kubeconfig .\kubeconfig_onyx -n milvus-operator patch milvus/onyx-azimuth-milvus-operator --type json --patch='[ { "op": "remove", "path": "/metadata/finalizers" } ]'

argocd --insecure login argocd.paas-purple.astrazeneca.net:443

argocd app list

argocd app get onyx-azimuth-milvus-operator

kubectl patch application onyx-azimuth-milvus-operator -n milvus-operator -p '{"metadata":{"finalizers":[]}}' --type merge

![alt text](image-4.png)

argocd cluster list