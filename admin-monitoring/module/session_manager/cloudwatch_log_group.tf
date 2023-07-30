data "aws_cloudwatch_log_group" "system_manager_cloudwatch" {
  name = "scsaas-cloudtrail-${var.aws_region}"
}

resource "aws_cloudwatch_log_subscription_filter" "logging" {
  depends_on      = [aws_lambda_permission.logging]
  destination_arn = aws_lambda_function.sessionManager_send_notification.arn
  filter_pattern  = "StartSession"
  log_group_name  = data.aws_cloudwatch_log_group.system_manager_cloudwatch.name
  name            = "logging_StartSession"
}
