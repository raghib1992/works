provider "aws" {
  region = "eu-north-1"
}

data "aws_ami" "wind" {
  most_recent      = true
  owners           = ["amazon"]

  filter {
    name   = "name"
    values = ["Windows_Server-2019-English-Full-Base-*"]
  }

#   filter {
#     name   = "root-device-type"
#     values = ["/dev/sda1"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   filter {
#     name   = "architecture"
#     values = ["x86_64"]
#   }
}

variable "admin_password" {}


resource "aws_instance" "name" {
    instance_type = "t3.micro"
    ami = data.aws_ami.wind.id
    user_data = file("${path.module}/sample.py")
    key_name = "stockholm"
    provisioner "file" {
        source      = "${path.module}/sample.py"
        destination = "C:/App/myapp.conf"

        connection {
            type     = "winrm"
            user     = "Administrator"
            password = "${var.admin_password}"
            host     = "${self.public_ip}"
        }
        }
}