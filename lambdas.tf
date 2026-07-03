resource "aws_lambda_function" "hello" {
  function_name = "hello_lambda"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "hello_lambda.lambda_handler"
  runtime = "python3.12"
}

resource "aws_lambda_function" "users" {
  function_name = "users-api"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "users.handler"
  runtime = "python3.12"
}