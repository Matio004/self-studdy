provider "aws" {
  region = "us-east-1"
}

# iam role
resource "aws_iam_role" "lambda_role" {
  name = "my-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# log policy
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role = aws_iam_role.lambda_role.name
  # arn:<partition>:<service>:<region>:<account_id>:<resource>
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "hello" {
  function_name = "hello_lambda"

  filename         = data.archive_file.lambda_hello.output_path
  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "hello_lambda.lambda_handler"
  runtime = "python3.12"
}

data "archive_file" "lambda_hello" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/src.zip"
}

resource "aws_apigatewayv2_api" "api" {
  name          = "hello-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.hello.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "hello" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default" # dzięku temu nie przeba pisać /prod/...
  auto_deploy = true
}

# uprawnienia dla apigw
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowInovke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}