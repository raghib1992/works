# resource "aws_ecs_service" "splunk-service" {
#   name            = "splunk-service"
#   launch_type     = "FARGATE" 
#   cluster         = aws_ecs_cluster.splunk-cluster.id
#   task_definition = aws_ecs_task_definition.test.arn
#   desired_count   = 1
# #   iam_role        = aws_iam_role.foo.arn
# #   depends_on      = [aws_iam_role_policy.foo]

#   # ordered_placement_strategy {
#   #   type  = "binpack"
#   #   field = "cpu"
#   # }
#   network_configuration {
#     subnets  = aws_subnet.private_subnet
#     security_groups = aws_security_group.splunk_ecs_sg.id
#     assign_public_ip = false
#   }
#   load_balancer {
#     target_group_arn = aws_alb_target_group.splunk-tg.arn
#     container_name   = "splunk"
#     container_port   = var.app_port
#   }

#   placement_constraints {
#     type       = "memberOf"
#     expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
#   }
# }