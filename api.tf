resource "aws_apigatewayv2_api" "api" {
  name          = "hello-api"
  protocol_type = "HTTP"
}

# uprawnienia dla apigw
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowInovke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}