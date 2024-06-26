# Argo Rollouts
1. Created Argo-rollouts Deployment and Service in Azimuth-profile/argo-rollouts Repo
2. Create Argo-rollouts-Dashboard deployment and service in Azimuth-Profile/argo-rollouts Repo
3. Create ArgoCd Application terragrunt file in Azimuth-Deployment/argo-rollouts/nonlive Repo


Argo Rollouts deploy to dev environment

### Step 1: Add argo rollouts helm official repository
- to argocd-project-configuration/terragrunt.hcl to add into argocd
github link *https://github.com/argoproj/argo-helm/tree/main/charts*

once you add helm repo it will show in app helm repo to add to create new app

### Step 2: Create docker image and push harbor repository
```
docker pull quay.io/argoproj/argo-rollouts:v1.6.6
docker tag quay.io/argoproj/argo-rollouts:v1.6.6 harbor.csis.astrazeneca.net/quay.io/argoproj/argo-rollouts:v1.6.6
docker push harbor.csis.astrazeneca.net/quay.io/argoproj/argo-rollouts:v1.6.6
```

### Step 3: Create terragrunt file to deploy argo-rollouts
- create new folder name argo-rollouts/nonlive and create create terrgrunt file to deploy argo-rollouts in nonlive cluster
	- To deploy in dev cluster, add dev cluster in cluster block
	```
	clusters = {
    	  dev-utils = {
     	    url  = "https://kube-api.paas-brown.astrazeneca.net:6443"
      	    env  = "dev"
      	    branch = "devel"
    	  }
  	}
	```
	- Change helm values
```
--set dashboard.eanble=true



    /*
#argo-rollout-dashboard = {
      priority        = "1"
      repo_url        = "https://github.com/AZU-IGNITE/azimuth.git"
      path            = "argo-rollouts"
      namespace       = ""
      clusters        = local.clusters
      plugin_name     = "argocd-vault-plugin-kustomize-v5_0_1"
    }
    */

    argo-rollout-dashboard = {
      priority        = "1"
      repo_url        = "https://github.com/AZU-IGNITE/azimuth.git"
      path            = "argo-rollouts"
      namespace       = ""
      clusters        = local.clusters
      plugin_name     = "argocd-vault-plugin-kustomize-v5_0_1"
    }

annotations = {
                kubernetes.io/ingress.class = "nginx"
                nginx.ingress.kubernetes.io/proxy-read-timeout = "180"
                nginx.ingress.kubernetes.io/proxy-send-timeout = "180"
                nginx.ingress.kubernetes.io/proxy-body-size = "600M"
              }

```
remove ingress
access - get pod and port forward from argo-rollouts
	create rolebinding, create 
terminal user do port-forward to namesopace
azimuth profile
get lates to main branch


```
argo-rollouts-nonlive = {
        priority        = "0"
        repo_url        = "https://argoproj.github.io/argo-helm"
        target_revision = "2.35.2"
        path            = "argo-rollouts"
        plugin_name     = "argocd-vault-plugin-helm"
        helm_args       = "--namespace argo-rollouts --include-crds"
        helm_values     = {
          clusterInstall = false
          controller = {
            image = {
              registry = "harbor.csis.astrazeneca.net/quay.io"
              tag      = "v1.6.6-new"
            }
          }
          dashboard = {
            enabled = false
            image = {
              registry = "harbor.csis.astrazeneca.net/quay.io"
              repository = "argoproj/kubectl-argo-rollouts"
            }
            ingress = {
              enabled = false
              hosts = [ "azimuth-argo-rollouts.paas-brown.astrazeneca.net" ]
              annotations = {
                "kubernetes.io/ingress.class"                    = "nginx"
                "nginx.ingress.kubernetes.io/proxy-read-timeout" = "180"
                "nginx.ingress.kubernetes.io/proxy-send-timeout" = "180"
                "nginx.ingress.kubernetes.io/proxy-body-size"    = "600M"
              }
            }
          }
        }
        clusters        = local.clusters
        namespace       = "argo-rollouts"
    }
```
kustomize build . > a.yaml

# ---
# apiVersion: networking.istio.io/v1alpha3
# kind: Gateway
# metadata:
#   name: istio-rollout-gateway
# spec:
#   selector:
#     istio: ingressgateway
#   servers:
#   - port:
#       number: 80
#       name: http
#       protocol: HTTP
#     hosts:
#     - "*"

