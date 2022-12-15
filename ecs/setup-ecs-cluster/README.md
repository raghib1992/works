ECS cluster are logical grouping of ec2 instance

1. You need a ecs cluster
2. setup iam
3. vpc
4. Create ECS Cluster (EC2 based)
- select the vpc 
- select the subnet
- Infrasucture
    * select Ec2
    * Create AutoScaling Group
    * Operating System 
    * Ec2 instance type
    * Desire Capacity 
    * SSh Keypair

5. Create ECS Cluster (fargate Based)
- select the vpc 
- select the subnet
- Infrasucture
    * select Fargate

6. Task defination
* Metadata in JSON format to tel ecs how to run a docker container
* Info Like 
    - Image name
    - port binging
    - memory and cpu reuired
    - env variable
    - Network Info
    - IAM Role
    - Logging Conf
    - Internet gateway

7. ECS service
* defien how many tasks should run and how they should be run 
* Ensure number of tasks desired is running across our fleet of ec2 instance
* They can be linked to Load Balaner if needed
* You can run tasks without service