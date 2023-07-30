variable "Lambda_accountLogin_principal" {
    description = "required Lambda permission principal"
}

variable "aws_region" {
    description = "get the name of the region from local file"
}

variable "sns_topic" {
    description = "get the name of the sns topic from the main module"
}

variable "caller_id" {
  description = "get the caller identity from main module"
}