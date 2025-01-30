1. Create eksctl cluser
eksctl create cluster --name=eksdemo --region=eu-north-1 --zones=eu-north-1a,eu-north-1b --version="1.27" --without-nodegroup
2. Create OIDC Provider
eksctl utils associate-iam-oidc-provider --region eu-north-1 --cluster eksdemo --approve
3. 