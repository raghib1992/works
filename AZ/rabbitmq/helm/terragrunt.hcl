terraform {
  source = "git::ssh://git@github.com/AZU-IGNITE/azimuth-terraform-modules.git//argocd-application-deployment?ref=v1.0.8"
}

locals {
  aws_region = "eu-west-1"

  clusters = {
    dev-azimuth = {
      url = "https://kube-api.paas-brown.astrazeneca.net:6443"
      env = "dev"
      branch = "main"
    }
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
}

provider "argocd" {
  server_addr = var.argocd_host
  username    = var.argocd_username
  password    = var.argocd_password
  insecure    = true
}
EOF
}

include {
  path = find_in_parent_folders()
}

inputs = {
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
          password = "<path:aiops/data/dev/rabbitmq#password>" #plugin in argocd help to fetch secret from vault
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
  }
}