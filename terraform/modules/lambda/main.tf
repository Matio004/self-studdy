resource "aws_lambda_function" "this" {
  function_name = var.function_name

  filename         = var.filename
  source_code_hash = base64sha256(var.filename)

  role    = var.role
  handler = var.handler
  runtime = var.runtime

  layers = var.layers

  environment {
    variables = var.enviroment_variables
  }
}

resource "aws_apigatewayv2_integration" "this" {
  api_id                 = var.api_gateway_id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.this.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${var.api_gateway_execution_arn}/*/*"
}
