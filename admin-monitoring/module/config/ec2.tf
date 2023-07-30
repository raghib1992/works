# data "aws_ami" "amazonLinux" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["amazonlinux2/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   owners = ["099720109477"] # Canonical
# }
provider "aws" {
    region = var.REGION
}

variable REGION {
  type        = string
  default     = "ap-south-1"
  description = "description"
}


# resource "aws_instance" "example" {
# #   ami           = data.aws_ami.ubuntu.id
#   ami = "ami-00bf4ae5a7909786c"
#   instance_type = "t3.micro"

#   tags = {
#     Name = "${var.REGION}-saas-member"
#   }
# }

# data "aws_instance" "foo" {
#   instance_id = "i-01f2d8c812cdd816f"

#   filter {
#     name   = "image-id"
#     values = ["ami-xxxxxxxx"]
#   }

#   filter {
#     name   = "tag:Name"
#     values = ["instance-name-tag"]
#   }
# }