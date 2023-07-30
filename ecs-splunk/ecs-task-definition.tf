resource "aws_ecs_task_definition" "test" {
  family                   = "splunk-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  task_role_arn            = aws_iam_role.ecs-efs-task-role.arn
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn
  container_definitions    = data.template_file.splunk-container-file.rendered

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  volume {
    name = "etc"

    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.splunk-efs.id
      transit_encryption      = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.splunk-ap.id
        iam             = "ENABLED"
      }
    }
  }
}

data "template_file" "splunk-container-file" {
  template = file("./splunkapp.json.tpl")

  vars = {
    # splunk-password = aws_secretsmanager_secret_version.splunk-secet-version.arn
    splunk-password = "Splunk-123"
  }
}
