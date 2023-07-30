provider "aws" {
  region = local.region
}

data "aws_caller_identity" "current" {}

terraform {
  # backend "s3" {
  #   bucket = "sc-saas-terraform"
  #   key = "global/us-west-2"
  #   region = "us-west-2"
  #   skip_credentials_validation = true
  # }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.46.0"
    }
  }
}