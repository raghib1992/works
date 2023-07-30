resource "aws_efs_file_system" "splunk-efs" {
  creation_token = "splunk-efs"

  tags = {
    Name = "splunk-efs"
  }
}

resource "aws_efs_mount_target" "splunk-efs-mount-target" {
  file_system_id = aws_efs_file_system.splunk-efs.id
  count          = "${length(var.private_subnets_cidr)}"
  subnet_id      = "${element(aws_subnet.public_subnet.*.id, count.index)}"
  security_groups = [ aws_security_group.efs-sg.id ]
}

resource "aws_efs_access_point" "splunk-ap" {
  file_system_id = aws_efs_file_system.splunk-efs.id
  posix_user {
    gid = 41812
    uid = 41812
  }
  root_directory {
    creation_info {
        owner_gid = 41812
        owner_uid = 41812
        permissions = 0766
    }
    path = "/splunk-etc"
  }
  tags = {
    "Name" = "splunk-ap"
  }
}