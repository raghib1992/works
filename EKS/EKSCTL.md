# Create Cluster
eksctl create cluster --name jenkins-eks-fg-raghib --region ap-south-1 --version 1.21 --fargate

# enable logging
eksctl utils update-cluster-logging --enable-types=all --region=ap-south-1 --cluster=jenkins-eks-fg-raghib --approve

# Associate OIDC
eksctl utils associate-iam-oidc-provider --region=ap-south-1 --cluster=jenkins-eks-fg-raghib --approve

# Create serviceAccount
eksctl create iamserviceaccount --attach-policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser --cluster jenkins-eks-fg-raghib --name jenkins-sa-ecr-raghib --namespace default --override-existing-serviceaccounts --region ap-south-1 --approve

################# 9th Oct 2021 ###############

#### Create iam role with name 

role name:- 
jenkins-eks-fg-raghib-system_masters

trust relationship:-
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:sts::288677030145:assumed-role/admins-from-gsuite/raghib.nadim@securecircle.com",
          "arn:aws:sts::288677030145:assumed-role/admins-from-gsuite/erik.webb@securecircle.com"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringLike": {
          "sts:RoleSessionName": "root"
        }
      }
    }
  ]
}

saml2aws exec -- aws sts get-caller-identity

saml2aws exec -- aws sts assume-role --role-arn "arn:aws:iam::288677030145:role/jenkins-eks-fg-raghib-system_masters" --role-session-name root

# Update aws-auth configmap in kube-system namespace

Granted system:masters access to arn:aws:iam::288677030145:role/admins-from-gsuite in aws-auth ConfigMap.

eksctl create iamidentitymapping --cluster jenkins-eks-fg-raghib --arn arn:aws:iam::288677030145:role/admins-from-gsuite --group system:masters --username "admins:gsuite:{{SessionName}}"


# Role arn:aws:iam::925201460575:role/jenkins-eks-fg-saas-01-ci_access was created allowing access from securecircle account (961831252000).  It has a policy allowing eks:DescribeCluster on the cluster.  arn:aws:iam::961831252000:role/rancher-instance-role was given access to sts:AssumeRole.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::961831252000:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}

# aws-auth ConfigMap was updated giving jenkins-eks-fg-saas-01-ci_access role system:masters on the cluster
eksctl create iamidentitymapping --cluster jenkins-eks-fg-raghib --arn arn:aws:iam::288677030145:role/jenkins-eks-fg-saas-01-ci_access --group system:masters --username "jenkins:master:{{SessionName}}"

# 

aws eks --region ap-south-1 update-kubeconfig --name jenkins-eks-fg-raghib --role-arn arn:aws:iam::288677030145:role/jenkins-eks-fg-saas-01-ci_access --dry-run

# kubectl config view

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://611C6D7DBE55B6B5070D56A44D8C3865.gr7.ap-south-1.eks.amazonaws.com
  name: jenkins-eks-fg-raghib.ap-south-1.eksctl.io
contexts:
- context:
    cluster: jenkins-eks-fg-raghib.ap-south-1.eksctl.io
    user: raghib.nadim@securecircle.com@jenkins-eks-fg-raghib.ap-south-1.eksctl.io
  name: raghib.nadim@securecircle.com@jenkins-eks-fg-raghib.ap-south-1.eksctl.io
current-context: raghib.nadim@securecircle.com@jenkins-eks-fg-raghib.ap-south-1.eksctl.io
kind: Config
preferences: {}
users:
- name: raghib.nadim@securecircle.com@jenkins-eks-fg-raghib.ap-south-1.eksctl.io
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - eks
      - get-token
      - --cluster-name
      - jenkins-eks-fg-raghib
      - --region
      - ap-south-1
      command: aws
      env:
      - name: AWS_STS_REGIONAL_ENDPOINTS
        value: regional
      provideClusterInfo: false
==================================================================================

# Role arn:aws:iam::<Account_B>:role/jenkins-eks-fg-raghib-ci_access was created allowing access from securecircle account (Account_A).  It has a policy allowing eks:DescribeCluster on the cluster.  arn:aws:iam::Account_A:role/rancher-instance-role was given access to sts:AssumeRole

# aws-auth ConfigMap was updated giving jenkins-eks-fg-raghib-ci_access role system:masters on the cluster
eksctl create iamidentitymapping --cluster jenkins-eks-fg-raghib --arn arn:aws:iam::Account_B:role/jenkins-eks-fg-raghib-ci_access --group system:masters --username "jenkins:master:{{SessionName}}"

# A kubeconfig was generated with AWS CLI
aws eks --region us-west-2 update-kubeconfig --name jenkins-eks-fg-raghib --role-arn arn:aws:iam::Account_B:role/jenkins-eks-fg-raghib-ci_access --dry-run

# Created role for “root” access to cluster
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:sts::<Account_B>:assumed-role/admins-from-gsuite/a@gmail.com"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringLike": {
          "sts:RoleSessionName": "root"
        }
      }
    }
  ]
}

# Granted system:masters access to arn:aws:iam:<account-ID>:role/admins-from-gsuite in aws-auth ConfigMap
eksctl create iamidentitymapping --cluster jenkins-eks-fg-raghib --arn arn:aws:iam::Account_B:role/admins-from-gsuite --group system:masters --username "admins:gsuite:{{SessionName}}"








# Create Cluster
eksctl create cluster --name jenkins-eks-fg-raghib --region ap-south-1 --version 1.21 --fargate

# associate OIDC to cluster
Ref- https://aws.amazon.com/blogs/containers/introducing-oidc-identity-provider-authentication-amazon-eks/
eksctl utils associate-iam-oidc-provider --region=ap-south-1 --cluster=raghib-eks-test --approve



# Created service account for access to ECR
eksctl create iamserviceaccount --attach-policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser --cluster jenkins-eks-fg-raghib --name jenkins-sa-ecr --namespace default --override-existing-serviceaccounts --region ap-south-1 --approve