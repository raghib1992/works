variable "SC_PURPOSE" {
    default = "trial"
    description = "select a tag to apply on specific instance"
}

variable "SecurityUpdateSNS" {
    default = "yumSecurityUpdateFailedNotification"
    description = "provide the name of the sns topic to get notification for security updates failed"
}