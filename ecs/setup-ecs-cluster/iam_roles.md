# creating iam roles
- ec2 roles
    1. Allow ecs agent ont he ec2 hosts to communicate with ecs and ecr

    ### Iam role -> aws service = ecs -> ec2 role for ecs -> Policy = AmazonEC2ContainerServiceforEC2Role

- ecs roles
    1. Roles which authorize ecs to manage resources on your behalf
    ### iam role -> aws sevice = ecs -> ecs -> policy = AmazonEC2ContainerServiceRole
- ecs task execution role
    1. role attach to ecs task
    ### iamorle -> aws service = ecs task -> policy = AmazonECSTaskExecutionRolePolicy
- auto scaling role
    1. Used to allow aws autoscaling to inspect stats and adjust scalable targets
    ### iam role-> aws service = ecs autoscale -> policy = AmazonEC2ContainerServiceAutoscaleRole
