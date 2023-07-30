resource "aws_iam_role" "ecs-execution-role" {
  name = "ecs-execution-role"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
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

resource "aws_iam_role_policy_attachment" "ecs-execution-attach" {
  role       = aws_iam_role.ecs-execution-role.name
  policy_arn = aws_iam_policy.ecs-execution-policy.arn
}


resource "aws_iam_policy" "ecs-execution-policy" {
  name        = "ecs-execution-policy"
  description = "ecs-efs-secret-manager-policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
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