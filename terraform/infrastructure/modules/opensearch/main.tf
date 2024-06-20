# Configure the AWS provider with a variable for the region
provider "aws" {
  region = "eu-west-3"
}

variable "collection_name" {
  type        = string
  default     = "example-collection"
  description = "Name of OpenSearch Serverless collection to create"
}

variable "index_name" {
  type        = string
  default     = "example-index"
  description = "Name of index created on OpenSearch Serverless collection"
}

# create encryption policy
resource "aws_opensearchserverless_security_policy" "example_encryption" {
  name        = "example"
  type        = "encryption"
  description = "encryption security policy"
  policy = jsonencode({
    Rules = [
      {
        Resource = [
          "collection/${var.collection_name}"
        ],
        ResourceType = "collection"
      }
    ],
    AWSOwnedKey = true
  })
}

# create network policy
resource "aws_opensearchserverless_security_policy" "example_network" {
  name        = "example"
  type        = "network"
  description = "network security policy"
  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "collection",
          Resource = [
            "collection/${var.collection_name}"
          ]
        }
      ],
      AllowFromPublic = true
    }
    ]
  )
}

# Use the ARN of the IAM user running Terraform in the data access policy
data "aws_caller_identity" "current" {}

# Create data access policy
resource "aws_opensearchserverless_access_policy" "example" {
  name        = "example"
  description = "example"
  type        = "data"
  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "index",
          Resource = [
            "index/${var.collection_name}/${var.index_name}"
          ],
          Permission = [
            "aoss:CreateIndex",
            "aoss:DeleteIndex",
            "aoss:UpdateIndex",
            "aoss:DescribeIndex",
            "aoss:ReadDocument",
          ]
        }
      ],
      Principal = [
        data.aws_caller_identity.current.arn
      ]
    }
  ])
}

# Create an AWS OpenSearch Serverless collection
resource "aws_opensearchserverless_collection" "example" {
  name             = var.collection_name
  description      = "example collection"
  type             = "SEARCH"
   # `aws_opensearchserverless_collection` resource documentation 
   # (https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearchserverless_collection),
   # You must create an encryption policy before creating an AWS OpenSearch Serverless collection.
   # If you have not created it, you will get the following error when you run terraform apply.
   # > ValidationException: No matching security policy of encryption type found for collection name: example_collection. 
   # Please create security policy of encryption type for this collection.
   depends_on = [aws_opensearchserverless_security_policy.example_encryption]
}

output "collection_endpoint" {
  value       = aws_opensearchserverless_collection.example.collection_endpoint
  description = "collection endpoint for created AWS OpenSearch Serverless collection"
}

output "collection_name" {
  value       = var.collection_name
  description = "Name of created Amazon OpenSearch Serverless collection"
}

output "index_name" {
  value       = var.index_name
  description = "Name of created index"
}
