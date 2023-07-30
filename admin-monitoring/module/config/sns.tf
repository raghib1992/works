data "aws_sns_topic" "yumSecurityUpdateFailedNotification" {
  name = var.SecurityUpdateSNS
}

resource "aws_sns_topic_subscription" "yumSecurityUpdateFailedsubcription" {
  topic_arn = data.aws_sns_topic.yumSecurityUpdateFailedNotification.arn
  protocol  = "email"
  endpoint  = "raghib.nadim@folium.cloud"
}