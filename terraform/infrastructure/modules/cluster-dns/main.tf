/*
* # Cluster DNS
* A module to create a DNS zone and certificate for the cluster.
*/

resource "aws_route53_zone" "zone" {
  name = var.cluster_dns_zone_name
}


# Create Certificate
resource "aws_acm_certificate" "wildcard_ssl_certificate" {
  domain_name               = var.cluster_dns_zone_name
  subject_alternative_names = ["*.${var.cluster_dns_zone_name}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}


# Define local "variable domain_to_validate"
locals {
  domain_to_validate = tolist(aws_acm_certificate.wildcard_ssl_certificate.domain_validation_options)[0]
}


# Define a resource to create a Route53 record for domain validation
resource "aws_route53_record" "validation_record" {
  name    = local.domain_to_validate.resource_record_name
  type    = local.domain_to_validate.resource_record_type
  zone_id = aws_route53_zone.zone.zone_id
  records = [local.domain_to_validate.resource_record_value]
  ttl     = 60
}

#Terraform configuration for creating a validation for an AWS ACMwildcard SSL 
# certificate using Route 53 DNS validation.
resource "aws_acm_certificate_validation" "wildcard_ssl_certificate_validation" {
  certificate_arn         = aws_acm_certificate.wildcard_ssl_certificate.arn
  validation_record_fqdns = [aws_route53_record.validation_record.fqdn]

  depends_on = [aws_route53_record.validation_record]
}
