module "sessionManager" {
    source ="./module/session_manager/"
    Lambda_principal = lookup(var.Principal_Region, local.region)
    aws_region = local.region
    sns_topic = aws_sns_topic.regional_saas_alerts
    caller_id = data.aws_caller_identity.current.id
}

module "accountLogin" {
    source = "./module/accountLogin/"
    Lambda_accountLogin_principal = lookup(var.Principal_Region, local.region)
    aws_region = local.region
    sns_topic = aws_sns_topic.regional_saas_alerts
    caller_id = data.aws_caller_identity.current.id
}
