# resource "aws_secretsmanager_secret" "splunk-secret" {
#   name = "splunk-secret"
# }

# resource "aws_secretsmanager_secret_version" "splunk-secet-version" {
#   secret_id     = aws_secretsmanager_secret.splunk-secret.id
#   secret_string = "Splunk-123"
# }

# output "secret" {
#   value = aws_secretsmanager_secret_version.splunk-secet-version
#   sensitive = true
# }