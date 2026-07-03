resource "aws_apigatewayv2_route" "hello" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "users" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /users"
  target    = "integrations/${aws_apigatewayv2_integration.users.id}"
}