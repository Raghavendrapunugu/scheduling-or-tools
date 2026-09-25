variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environments" {
  type    = list(string)
  default = ["dev", "uat", "prod"]
}