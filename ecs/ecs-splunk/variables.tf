variable "aws_region" {}

variable "vpc_cidr" {
  default = "10.150.0.0/22"
}

# variable "aws_profile" {
#   default = "default"
# }

variable "env" {
  default = "test"
}

variable "server-name" {
  default = "splunk"
}

variable "public_subnets_cidr" {
    default = [ "10.150.0.0/24", "10.150.1.0/24" ]
}

variable "private_subnets_cidr" {
    default = [ "10.150.2.0/24", "10.150.3.0/24" ]  
}

variable "availability_zones" {
    default = ["ap-south-1a","ap-south-1b"] 
}

# variable "health_check_path" {
#   default = "/en-US/account/login?return_to=%2Fen-US%2F"
# }

variable "app_port" {
  default = 8000
}

variable "alb_port" {
  default = 80
}

# variable "aws_key" {
  
# }

# variable "aws_secret" {
  
# }

# variable "splunk-key" {
#   default = "Splunk-123"
# }