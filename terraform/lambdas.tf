resource "aws_lambda_function" "hello" {
  function_name = "hello_lambda"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.shows"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.series_by_name.name
    }
  }
}

resource "aws_lambda_function" "users" {
  function_name = "users-api"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "users.handler"
  runtime = "python3.12"
}

resource "aws_lambda_function" "seasons" {
  function_name = "seasons"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.seasons"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.series_by_name.name
    }
  }
}

resource "aws_lambda_function" "episodes" {
  function_name = "episodes"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.episodes"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.series_by_name.name
    }
  }
}