# LB for EC2
- Bridge netwroking mode and get dynamic port mapping
- allow on ec2 instances sg any port from the alb

# LB for Fargate
- Use awsvpc netwrking mode
- each task has a unique IP
- allow on ENI's sg "the task port" from the ALB sg's

