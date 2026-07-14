provider "aws" {
  region = "us-east-1"
}

data "archive_file" "lambda_hello" {
  type        = "zip"
  source_dir  = "${path.module}/../bootstrap"
  output_path = "${path.module}/../bootstrap.zip"
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../bootstrap-layer"
  output_path = "${path.module}/../bootstrap-layer.zip"
}

resource "aws_lambda_layer_version" "python_dependencies" {
  filename            = data.archive_file.layer_zip.output_path
  layer_name          = "python-dependencies"
  compatible_runtimes = ["python3.12"]

  source_code_hash = data.archive_file.layer_zip.output_base64sha256
}

resource "aws_lambda_layer_version" "common" {
  layer_name          = "common"
  filename            = "../bootstrap-layer.zip"
  compatible_runtimes = ["python3.13"]
}

