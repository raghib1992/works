provider "aws" {
  region = local.region
  profile = "default"
  # access_key = var.aws_key
  # secret_key = var.aws_secret
}

data "aws_caller_identity" "current" {}

locals {
#   common_tags = {
#     sc_purpose = "sc-saas"
#   }
  region = var.aws_region
#   domainname = "us2.saas.securecircle.com"
#   route53_zone_id = "Z1OKQMPVBW4QXC"
}

# terraform {
#   backend "s3" {
#     bucket = "sc-saas-terraform"
#     key = "global/us-west-2"
#     region = "us-west-2"
#     skip_credentials_validation = true
#   }
#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 3.46.0"
#     }
#   }
# }