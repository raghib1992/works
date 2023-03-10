provider "aws" {
  region = local.region
}

locals {
  common_tags = {
    env = "raghib-test"
  }
  region          = "ap-south-1"
#   domainname      = "us2.saas.securecircle.com"
#   route53_zone_id = "Z1OKQMPVBW4QXC"
}