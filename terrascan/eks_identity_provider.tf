resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = []
  url             = aws_eks_cluster.jenkins-eks-fg-saas-01.identity.0.oidc.0.issuer
}