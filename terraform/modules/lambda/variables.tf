
variable "function_name" {
  type = string
}

variable "filename" {
  type = string
}

variable "handler" {
  type = string
}

variable "runtime" {
  type = string
}

variable "role" {
  type = string
}

variable "layers" {
  type    = list(string)
  default = []
}

variable "enviroment_variables" {
  type    = map(string)
  default = {}
}

variable "api_gateway_id" {
  type = string
}

variable "api_gateway_execution_arn" {
  type = string
}
