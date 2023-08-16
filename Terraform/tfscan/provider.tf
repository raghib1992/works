provider "aws" {
  region = local.region
}

locals {
  common_tags = {
    env = "raghib-test"
  }
  region = "ap-south-1"
}