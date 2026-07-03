resource "aws_apigatewayv2_api" "api" {
  name          = "hello-api"
  protocol_type = "HTTP"
}

