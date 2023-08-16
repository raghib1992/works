resource "aws_iam_role" "ecs-efs-task-role" {
  name = "ecs-efs-task-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-efs-attach" {
  role       = aws_iam_role.ecs-efs-task-role.name
  policy_arn = aws_iam_policy.ecs-efs-policy.arn
}


resource "aws_iam_policy" "ecs-efs-policy" {
  name        = "ecs-efs-policy"
  description = "ecs-efs-secret-manager-policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticfilesystem:ClientMount",
                "elasticfilesystem:ClientWrite"
            ],
            "Resource": "arn:aws:elasticfilesystem:*:566881612178:file-system/*",
            "Condition": {
                "StringEquals": {
                    "elasticfilesystem:AccessPointArn":"arn:aws:elasticfilesystem:*:566881612178:access-point/*"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:*:*:secret:SPLUNK_PASSWORD*"
            ]
        }
    ]
}
EOF
}