locals {
  inbound_ports = [443]
}

resource "aws_security_group" "lb_sg" {
  vpc_id = var.vpc_id

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  dynamic "ingress" {
    for_each = local.inbound_ports
    content {
      from_port = ingress.value
      to_port = ingress.value
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    
  }
}