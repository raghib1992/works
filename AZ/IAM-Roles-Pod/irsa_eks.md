1. Create eksctl cluser
eksctl create cluster --name=eksdemo --region=eu-north-1 --zones=eu-north-1a,eu-north-1b --version="1.27" --without-nodegroup
2. Create OIDC Provider
eksctl utils associate-iam-oidc-provider --region eu-north-1 --cluster eksdemo --approve
3. Create IAM policy 
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::raghib-irsa-demo-bucket"
            ]
        }
    ]
}
```
4. Create bucket
5. Create sa
```sh
kubectl apply -f .\manifesrs\irsa-sa.yaml
```
6. Create trust relatioship
- which resource have ability to assume role
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::796973483652:oidc-provider/<OIDC_PROVIDER>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<OIDC_PROVIDER>:aud": "sts.amazonaws.com",
          "<OIDC_PROVIDER>:sub": "system:serviceaccount:<NAMESPACE>:<SERVICE_ACCOUNT>"
        }
      }
    }
  ]
}
```
```sh
aws iam create-role --role-name my-s3-access-role --assume-role-policy-document file://trust-relationship.json

aws iam attach-role-policy --role-name my-s3-access-role --policy-arn=arn:aws:iam::796973483652:policy/my-s3-access-role
```
7. annotate serviceaccount
```sh
kubectl annotate serviceaccount irsa-sa eks.amazonaws.com/role-arn=arn:aws:iam::796973483652:policy/my-s3-access-role
```