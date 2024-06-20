provider "aws" {
  region = "eu-west-3"
}

locals {
   name = "dev-cluster"
}

module "key_pair" {
  source  = "terraform-aws-modules/key-pair/aws"
  key_name_prefix    = local.name
  create_private_key = true
}

resource "tls_private_key" "ssh_private_key" {
  algorithm   = "RSA"
  rsa_bits    = 2048
}

resource "aws_secretsmanager_secret" "ssh_private_key_secret" {
 name = "${local.name}-ssh-private-key"
}

resource "aws_secretsmanager_secret_version" "ssh_private_key_secret_version" {
  secret_id     = aws_secretsmanager_secret.ssh_private_key_secret.id
  secret_string = module.key_pair.private_key_openssh
}

output "ssh_private_key_secret_name" {
  value = aws_secretsmanager_secret.ssh_private_key_secret.name
}
output "ssh_private_key_name" {
  value = module.key_pair.key_pair_name
}

# USE : AWS_PROFILE=vev-dev aws secretsmanager get-secret-value --secret-id dev-cluster-ssh-private-key  --region eu-west-3
