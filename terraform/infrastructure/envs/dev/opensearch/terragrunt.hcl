# Include shared configurations from the dev level
include {
  path = find_in_parent_folders()
}

# Define Terragrunt configurations for the current directory
terraform {
  source = "../../../modules/opensearch"
}

inputs = {
   region = "eu-west-3"
   cidr_block = "10.0.0.0/16"
}
