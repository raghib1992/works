resource "aws_security_group" "splunk-container" {
  name        = "splunk-container"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 8000
    to_port          = 8000
    protocol         = "tcp"
    cidr_blocks      = [aws_vpc.vpc.cidr_block]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "splunk-container"
  }
}

resource "aws_security_group" "efs-sg" {
  name        = "efs-sg"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 2049
    to_port          = 2049
    protocol         = "tcp"
    # cidr_blocks      = [aws_vpc.vpc.cidr_block]
    security_groups = [ aws_security_group.splunk-container.id ]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "efs-sg"
  }
}

resource "aws_security_group" "splunk_ecs_sg" {
  name = "splunk_ecs_sg"
}

# Allow scripts and file upload
# resource "aws_security_group_rule" "in_ssh" {
#   from_port = 22
#   protocol = "tcp"
#   security_group_id = "${aws_security_group.splunk_sg.id}"
#   cidr_blocks = ["${var.terraform_plublic_ip}"]
#   to_port = 22
#   type = "ingress"
# }

resource "aws_security_group_rule" "splunk-sg-rule" {
  from_port = var.app_port
  protocol = "tcp"
  security_group_id = "${aws_security_group.splunk_ecs_sg.id}"
  source_security_group_id = aws_security_group.splunk_alb_sg.id
  to_port = var.app_port
  type = "ingress"
}

# Allow for apt to run and install
# resource "aws_security_group_rule" "ext_any" {
#   from_port = 80
#   protocol = "tcp"
#   security_group_id = "${aws_security_group.splunk_sg.id}"
#   cidr_blocks = ["0.0.0.0/0"]
#   to_port = 80
#   type = "egress"
# }
# Allow for splunk to get addons
# resource "aws_security_group_rule" "ext_any_addon" {
#   from_port = 443
#   protocol = "tcp"
#   security_group_id = "${aws_security_group.splunk_sg.id}"
#   cidr_blocks = ["0.0.0.0/0"]
#   to_port = 443
#   type = "egress"
# }

# allow web
# resource "aws_security_group_rule" "lb_to_instance" {
#   from_port = 443
#   protocol = "tcp"
#   security_group_id = "${aws_security_group.splunk_sg.id}"
#   source_security_group_id = "${aws_security_group.splunk_lb_sg.id}"
#   to_port = 443
#   type = "ingress"
# }

# allow HEC
# resource "aws_security_group_rule" "hec_lb_to_instance" {
#   from_port = 8088
#   protocol = "tcp"
#   security_group_id = "${aws_security_group.splunk_sg.id}"
#   source_security_group_id = "${aws_security_group.splunk_hec_lb_sg.id}"
#   to_port = 8088
#   type = "ingress"
# }

# Create the web LB SG
resource "aws_security_group" "splunk_alb_sg" {
  name = "splunk_lb_sg"

  ingress {
    protocol = "tcp"
    from_port = var.alb_port
    to_port = var.alb_port
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    protocol = "tcp"
    from_port = var.app_port
    to_port = var.app_port
    security_groups = ["${aws_security_group.splunk_ecs_sg.id}"]
  }
}

# Create the hec LB SG
# resource "aws_security_group" "splunk_hec_lb_sg" {
#   name = "splunk_hec_lb_sg"

#   # Allows ingress from aws firehose US East (N. Virginia)
#   ingress {
#     protocol = "tcp"
#     from_port = 8088
#     to_port = 8088
#     cidr_blocks = "${var.splunk_hec_sources}"
#   }
#   ingress {
#     from_port = 8088
#     protocol = "tcp"
#     to_port = 8088
#     cidr_blocks = ["${var.terraform_plublic_ip}"]
#   }
#   egress {
#     protocol = "tcp"
#     from_port = 8088
#     to_port = 8088
#     security_groups = ["${aws_security_group.splunk_sg.id}"]
#   }
# }