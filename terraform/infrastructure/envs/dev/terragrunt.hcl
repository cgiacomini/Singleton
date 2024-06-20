
# Terragrunt configurations specific to the dev environment

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket         = "opensearch-terraform-state-dev"
    region         = "eu-west-3"
    dynamodb_table = "opensearch-terraform-state-dev-table"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    profile        = "singleton"
  }
}

terraform {
  extra_arguments "retry_lock" {
    commands  = get_terraform_commands_that_need_locking()
    arguments = ["-lock-timeout=20m"]
  }

  extra_arguments "aws_profile" {
    commands  = get_terraform_commands_that_need_vars()
    arguments = []
    env_vars = {
      AWS_PROFILE = "singleton"
    }
  }
}
