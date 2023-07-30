
variable "Lambda_principal" {
    description = "required Lambda permission principal"
}

variable "aws_region" {
    description = "get the region from local file from main module"
}

variable "sns_topic" {
    description = "get the sns topic from main module"
}

variable "caller_id" {
    description = "get the caller id from main module"
}