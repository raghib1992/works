resource "aws_sns_topic" "regional_saas_alerts" {
  display_name = "${local.region} - SecureCircle regional SaaS alerts"
  name = "${local.region}-saas-alerts-sns-topic"
  tags = local.common_tags
}

resource "aws_sns_topic_subscription" "AccessKeyIdRotation" {
  topic_arn = aws_sns_topic.regional_saas_alerts.arn
  protocol  = "email"
  endpoint  = "raghib.nadim@securecircle.com"
}
