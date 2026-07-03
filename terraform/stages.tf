resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default" # dzięku temu nie przeba pisać /prod/...
  auto_deploy = true
}