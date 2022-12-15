# creating iam roles
- ec2 roles
    1. Used by Ecs agent in Ec2 host
    2. Make API call to ECS service 
    3. Send Logs to Cloud Watch Logs
    4. Pulldocker Image from ECR

    ### Iam role -> aws service = ecs -> ec2 role for ecs -> Policy = AmazonEC2ContainerServiceforEC2Role

- ecs roles
    1. Roles which authorize ecs to manage resources on your behalf
    ### iam role -> aws sevice = ecs -> ecs -> policy = AmazonEC2ContainerServiceRole
- ecs task execution role
    1. role attach to ecs task
    2. Alow each task to have specific role
    3. Use different role for different ecs service
    4. Task role define in TAsk definition
    ### iamorle -> aws service = ecs task -> policy = AmazonECSTaskExecutionRolePolicy
- auto scaling role
    1. Used to allow aws autoscaling to inspect stats and adjust scalable targets
    ### iam role-> aws service = ecs autoscale -> policy = AmazonEC2ContainerServiceAutoscaleRole
