# resource "aws_ssm_association" "example" {
#   name = aws_ssm_document.yumSecurityUpdate.name
#   association_name = "yumSecurityUpdateEC2"
#   compliance_severity = "HIGH"
#   schedule_expression = "cron(0 */30 * * * ? *)"
#   max_concurrency = 1
#   max_errors = 0
#   apply_only_at_cron_interval = true

#   # AWS currently supports a maximum of 5 targets.
#   targets {
#     key    = "InstanceIds"
#     values = [data.aws_instance.foo.id]
#   }
# }

# resource "aws_ssm_document" "yumSecurityUpdate" {
#   name          = "yumSecurityUpdate"
#   document_type = "Command"

#   content = <<DOC
#   {
#     "schemaVersion": "1.2",
#     "description": "yum update the security configuratio of the ec2",
#     "parameters": {

#     },
#     "runtimeConfig": {
#       "aws:runShellScript": {
#         "properties": [
#           {
#             "id": "0.aws:runShellScript",
#             "runCommand": ["yum -t -y --exclude=kernel --exclude=nvidia* --exclude=cuda* --security --sec-severity=critical --sec-severity=important upgrade"]
#           }
#         ]
#       }
#     }
#   }
# DOC
# }