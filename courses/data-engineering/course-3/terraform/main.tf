terraform {
  required_providers {
    minio = {
      source = "aminueza/minio"
      version = ">= 2.0.0"
    }
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = ">= 1.13.0"
    }
  }
}

provider "minio" {
  minio_server   = "localhost:9000"
  minio_user     = var.minio_access_key
  minio_password = var.minio_secret_key
}

resource "minio_s3_bucket" "store_bucket" {
  bucket = "store-bucket"
  acl    = "private"
}

# Upload all JSON files from the data/ folder
locals {
  json_files = fileset("${path.module}/data", "*.json")
}

resource "minio_s3_object" "json_objects" {
  for_each = { for file in local.json_files : file => file }
  object_name = "${each.key}"
  bucket_name = minio_s3_bucket.store_bucket.bucket
  source = "${path.module}/data/${each.value}"
  content_type = "application/json"
}


provider "postgresql" {
  host            = "localhost"
  port            = 5432
  username        = var.postgres_user
  password        = var.postgres_password
  database        = "postgres"
  sslmode         = "disable"
}

resource "postgresql_database" "analytic-db" {
  name = "analytics"
}
