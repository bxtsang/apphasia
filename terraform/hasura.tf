variable "region" {}
variable "domain" {}
variable "hasura_admin_secret" {}
variable "hasura_jwt_secret_algo" {}
variable "hasura_jwt_secret_key" {}
variable "rds_username" {}
variable "rds_password" {}
variable "ecs_cluster_name" {}

module "hasura" {
  source                          = "Rayraegah/hasura/aws"
  version                         = "3.1.1"
  region                          = var.region
  domain                          = var.domain
  hasura_admin_secret             = var.hasura_admin_secret
  hasura_jwt_secret_algo          = var.hasura_jwt_secret_algo
  hasura_jwt_secret_key           = var.hasura_jwt_secret_key
  hasura_console_enabled          = "false"
  rds_db_name                     = "aphasiaSG"
  rds_instance                    = "db.t3.micro"
  rds_username                    = var.rds_username
  rds_password                    = var.rds_password
  rds_storage_encrypted           = "true"
  multi_az                        = "true"
  az_count                        = "2"
  vpc_enable_dns_hostnames        = "false"
  ecs_cluster_name                = var.ecs_cluster_name
  create_iam_service_linked_role = false

}

provider "aws" {
    region = "ap-southeast-1"
}