Steps
# WandB
### **Steps**
- Raise a SNOW Ticket for S3 bucket creation (RITM5696282)
- Enable CORS
```json
[
{
"AllowedHeaders": [
"*"
],
"AllowedMethods": [
"GET",
"PUT"
],
"AllowedOrigins": [
"https://dev-azimuth-wandb.paas-brown.astrazeneca.net"
],
"ExposeHeaders": []
}
]
```
- wandb login --relogin --host=https://dev-azimuth-wandb.paas-brown.astrazeneca.net
- AWS RDS MySQL → Raise Infrastructure Demand ticket in SNOW (IDMD0011409)
  - https://azprod.service-now.com/askaz/?id=sc_cat_item&sys_id=8035823c0f9d8680fee2df94e2050ec5
  - Configure DB
    - Install MySql Client → https://mariadb.com/resources/blog/installing-mariadb-10-1-16-on-mac-os-x-with-homebrew/ 
    - mysql -h iecdazmthdevdb01.c008ssgujac3.eu-west-1.rds.amazonaws.com -P 3306 -u admin -p
    ```
    CREATE USER 'wandb_local_dev'@'%' IDENTIFIED BY 'wandb_local_dev';
    CREATE DATABASE wandb_local_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    GRANT ALL ON wandb_local_dev.* TO 'wandb_local_dev'@'%' WITH GRANT OPTION;

    use wandb_local_dev;
    show tables;
    select * from entities;
    select * from teams;
    select * from users;
    select * from projects;
    ```


# Update WandB Container Image
### Step 1: Check the latest wandb/local tag in dockerhub repository
- Link: *https://hub.docker.com/r/wandb/local/tags*
### Step 2: Pull the latest tag image to local
```sh
docker pull wandb/local:0.51.1
# replace version tag with latest
```
### Step 3: Tag the container image with harbor repository and push to harbor repository
```sh
docker login harbor.csis.mrndevops.in
docker tag wandb/local:0.51.1 harbor.csis.mrndevops.in/wandb/local:0.51.1
docker push harbor.csis.mrndevops.in/wandb/local:0.51.1
```
### Step 4: Pull azimuth repository to local machine, if available in local, pull latest commit
```sh
# To clone repo to local machine
git clone https://github.com/azu-ignite/azimuth.git
 
# To pull latest commit of devel branch
git pull origin devel
```
### Step 5: Create new branch from devel as base branch
```sh
git checkout -b AZK-559
# replace AZK-559 with your new branch name
```
### Step 6: First do changes in dev cluster
- update images.newTag in file wandb\dev\kustomization.yaml
- Example
```yml
resources:
  - namespace.yaml
  - secrets.yaml
  - deployment.yaml
  - service.yaml
  - ingress.yaml
 
images:
  - name: wandb/local
    newName: harbor.csis.astrazeneca.net/wandb/local
    # Replace newTag with latest tag in below line
    newTag: 0.51.1
```
### Step 7:  Push the changes to remote repo
```sh
git add wandb\dev\kustomization.yaml
git commit -m "update dev cluster wandb conatiner image to 0.51.1"
git push -u origin AZK-559
```
### Step 8: Create Merge Request in Github
- source branch: AZK-559 ; Destination branch: devel
### Step 9: Once MR is approved 
- Merge the MR
- Verify the changes is successfully deploy in  ArgoCD,
- In AegoCD: filter Cluster : bronze, search for application: dev-azimuth-admission-webhook-nonlive
### Step 10: Now repeat step 6 to step 9  for iron, bronze and lead cluster

