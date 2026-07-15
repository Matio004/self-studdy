output "api_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "lambda_functions" {
  value = {
    get_show     = module.hello.function_name
    get_seasons  = module.seasons.function_name
    get_episodes = module.episodes.function_name
    delete_show  = module.delete_show.function_name
    post_show    = module.create_show.function_name
    post_season  = module.create_season.function_name
    post_episode = module.create_episode.function_name
  }
}

output "common_layer_name" {
  value = aws_lambda_layer_version.common.layer_name
}

output "dependencies_layer_name" {
  value = aws_lambda_layer_version.python_dependencies.layer_name
}
