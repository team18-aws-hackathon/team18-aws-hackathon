terraform {
  backend "s3" {
    bucket       = "team18-terraform-state-740d78b6"
    key          = "dev/terraform.tfstate"
    region       = "us-east-1"
    dynamodb_table = "team18-terraform-locks"
    encrypt      = true
  }
}