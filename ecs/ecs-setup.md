# Task /Service Setup - Hands-on I/II
### Launch Container on Fargate
### Step 1: Create Task definition
1. container name
2. image uri = docker pull pauloclouddev/wisdom-img (docker)
3. App Environment select fargate
4. opertaing system
5. cpu
6. memory
7. Task role select ecs task role
8. network mode select awsvpc

### Step 2: Create Task without Service
* Deployment configuration
1. Select Task 
2. In task definition select the task definition created in last steps
* Networking
1. vpc and subnet select the vpc created for this cluster
2. Create sg
- add rule HTTP port 80 open to all (0.0.0.0/0)

### Step 2: create task and service
* Deployment configuration
1. Select Service
2. service name 
3. In task definition select the task definition created in last steps
* Networking
1. vpc and subnet select the vpc created for this cluster
2. Create/select existing  sg
*****************************************************
### Launch Container on EC2
### Step 1: Create Task definition
1. container name
2. image uri = docker pull pauloclouddev/wisdom-img (docker)
3. App Environment select fargate
4. opertaing system
5. cpu
6. memory
7. Task role select ecs task role
8. network mode select awsvpc

### Step 2: Create Task without Service
* Deployment configuration
1. Select Task 
2. In task definition select the task definition created in last steps
* Networking
1. vpc and subnet select the vpc created for this cluster
2. Create sg
- add rule HTTP port 80 open to all (0.0.0.0/0)

### Step 2: create task and service
* Deployment configuration
1. Select Service
2. service name 
3. In task definition select the task definition created in last steps
* Networking
1. vpc and subnet select the vpc created for this cluster
2. Create/select existing  sg

