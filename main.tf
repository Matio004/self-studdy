provider "aws" {
  region = "us-east-1"
}

data "archive_file" "lambda_hello" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/src.zip"
}
