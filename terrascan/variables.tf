variable "vpc_cidr_block" {
  type        = string
  default     = "192.168.0.0/16"
  description = "VPC CIDR Block"
}

variable "private_subnet_cidrs" {
  type = list(string)
  default = [
    "192.168.96.0/19",
    "192.168.128.0/19",
    "192.168.160.0/19"
  ]
  description = "Subnet ranges"
}

variable "public_subnet_cidrs" {
  type = list(string)
  default = [
    "192.168.0.0/19",
    "192.168.64.0/19",
    "192.168.32.0/19"
  ]
  description = "Subnet ranges"
}
