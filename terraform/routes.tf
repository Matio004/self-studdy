resource "aws_apigatewayv2_route" "shows_by_name" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /shows/{name}"
  target    = "integrations/${module.hello.integration_id}"
}

resource "aws_apigatewayv2_route" "seasons_by_name" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /shows/{name}/seasons"
  target    = "integrations/${module.seasons.integration_id}"
}

resource "aws_apigatewayv2_route" "episodes_by_season" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /shows/{name}/seasons/{season}"
  target    = "integrations/${module.episodes.integration_id}"
}

resource "aws_apigatewayv2_route" "delete_show" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "DELETE /shows/{name}"
  target    = "integrations/${module.delete_show.integration_id}"
}

resource "aws_apigatewayv2_route" "post_show" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /shows"
  target    = "integrations/${module.create_show.integration_id}"
}

resource "aws_apigatewayv2_route" "post_season" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /shows/{name}/seasons"
  target    = "integrations/${module.create_season.integration_id}"
}

resource "aws_apigatewayv2_route" "post_episode" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /shows/{name}/seasons/{season}"
  target    = "integrations/${module.create_episode.integration_id}"
}

