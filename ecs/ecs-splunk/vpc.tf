/*==== The VPC ======*/
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
#   enable_dns_hostnames = var.enable_hostname
#   enable_dns_support   = var.enable_dns_support
  tags = {
    Name = "${var.server-name}-vpc"
    env  = var.env
  }
}

/*==== Subnets ======*/
/* Internet gateway for the public subnet */
resource "aws_internet_gateway" "ig" {
  vpc_id = "${aws_vpc.vpc.id}"
  tags = {
    Name = "${var.server-name}-igw"
    env  = var.env
  }
}

/* Elastic IP for NAT */
resource "aws_eip" "nat_eip" {
  vpc        = true
  count      = "${length(var.public_subnets_cidr)}"
  depends_on = [aws_internet_gateway.ig]
  tags = {
    Name = "${var.server-name}-${element(var.availability_zones, count.index)}-eip"
    env  = var.env
  }
}

/* NAT */
resource "aws_nat_gateway" "nat" {
  # allocation_id = "${aws_eip.nat_eip.id}"
  allocation_id = "${element(aws_eip.nat_eip.*.id, count.index)}"
  count         = "${length(var.public_subnets_cidr)}"
  # subnet_id     = "${aws_subnet.public_subnet.*.id}"
  subnet_id     = "${element(aws_subnet.public_subnet.*.id, count.index)}"
  depends_on    = [aws_internet_gateway.ig]
  tags = {
    Name  = "${var.server-name}-nat"
    env   = var.env
  }
}

/* Public subnet */
resource "aws_subnet" "public_subnet" {
  vpc_id                  = "${aws_vpc.vpc.id}"
  count                   = "${length(var.public_subnets_cidr)}"
  cidr_block              = "${element(var.public_subnets_cidr,   count.index)}"
  availability_zone       = "${element(var.availability_zones,   count.index)}"
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.server-name}-${element(var.availability_zones, count.index)}-public-subnet"
    env  = "${var.env}"
  }
}

/* Private subnet */
resource "aws_subnet" "private_subnet" {
  vpc_id                  = "${aws_vpc.vpc.id}"
  count                   = "${length(var.private_subnets_cidr)}"
  cidr_block              = "${element(var.private_subnets_cidr, count.index)}"
  availability_zone       = "${element(var.availability_zones,   count.index)}"
  map_public_ip_on_launch = false
  tags = {
    Name = "${var.server-name}-${element(var.availability_zones, count.index)}-private-subnet"
    env  = "${var.env}"
  }
}

## ********************************************
/* Routing table for public subnet */
resource "aws_route_table" "public" {
  vpc_id = "${aws_vpc.vpc.id}"
  tags = {
    Name = "${var.server-name}-public-route-table"
    env  = "${var.env}"
  }
}
resource "aws_route" "public_internet_gateway" {
  route_table_id         = "${aws_route_table.public.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.ig.id}"
}
/* Route table associations */
resource "aws_route_table_association" "public" {
  count = "${length(var.public_subnets_cidr)}"
  subnet_id      = "${element(aws_subnet.public_subnet.*.id, count.index)}"
  route_table_id = "${aws_route_table.public.id}"
}
# ************************************************

# /* Routing table for private subnet */
resource "aws_route_table" "private" {
  vpc_id = "${aws_vpc.vpc.id}"
  count  = "${length(var.private_subnets_cidr)}"
  tags = {
    Name = "${var.server-name}-private-route-table"
    env  = "${var.env}"
  }
}
resource "aws_route" "private_nat_gateway" {
  count                  = "${length(var.private_subnets_cidr)}"
  route_table_id         = "${element(aws_route_table.private.*.id, count.index)}"
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = "${element(aws_nat_gateway.nat.*.id, count.index)}"
}
resource "aws_route_table_association" "private" {
  count          = "${length(var.private_subnets_cidr)}"
  subnet_id      = "${element(aws_subnet.private_subnet.*.id, count.index)}"
  route_table_id = "${element(aws_route_table.private.*.id, count.index)}"
}

# /*==== VPC's Default Security Group ======*/
# resource "aws_security_group" "default" {
#   name        = "${var.env}-default-sg"
#   description = "Default security group to allow inbound/outbound from the VPC"
#   vpc_id      = "${aws_vpc.vpc.id}"
#   depends_on  = [aws_vpc.vpc]
#   ingress {
#     from_port = "0"
#     to_port   = "0"
#     protocol  = "-1"
#     self      = true
#   }
  
#   egress {
#     from_port = "0"
#     to_port   = "0"
#     protocol  = "-1"
#     self      = "true"
#   }
#   tags = {
#     env = "${var.env}"
#   }
# }