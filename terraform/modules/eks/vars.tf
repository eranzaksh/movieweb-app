variable "private_subnet_ids" {
  description = "Private Subnet IDs"
  type        = list(string)
}
variable "vpc_id" {
  type = string
}

variable "lb_sg_id" {
  type = string
}