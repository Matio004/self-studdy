resource "aws_apigatewayv2_route" "shows_by_name" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /shows/{name}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "users" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /users"
  target    = "integrations/${aws_apigatewayv2_integration.users.id}"
}

resource "aws_apigatewayv2_route" "seasons_by_name" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /seasons/{name}"
  target    = "integrations/${aws_apigatewayv2_integration.seasons.id}"
}