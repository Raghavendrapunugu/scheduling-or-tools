terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "wfm_app" {
  name                 = "wfm-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "wfm_clusters" {
  for_each = toset(var.environments)
  name     = "wfm-${each.key}-cluster"
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  for_each          = toset(var.environments)
  name              = "/ecs/wfm-${each.key}"
  retention_in_days = 14
}