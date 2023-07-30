resource "aws_cloudwatch_log_group" "trail_consoleLog_data" {
  name = "scsaas-cloudtrail-${var.aws_region}"
}

resource "aws_cloudwatch_log_subscription_filter" "logging" {
  depends_on      = [aws_lambda_permission.logging]
  destination_arn = aws_lambda_function.accountLogin_send_notification.arn
  filter_pattern  = "ConsoleLogin"
  log_group_name  = aws_cloudwatch_log_group.trail_consoleLog_data.name
  name            = "logging_ConsoleLogin"
}
