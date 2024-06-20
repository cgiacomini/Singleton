generate "provider" {
  path = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
provider "aws" {
  region = "eu-west-3"
}
EOF
}

include {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules//cluster-dns"
}

inputs = {
  cluster_dns_zone_name = "singleton.com"
}
