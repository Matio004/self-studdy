module "hello" {
  source = "./modules/lambda"

  function_name = "hello_lambda"
  filename      = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.shows"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}

module "seasons" {
  source = "./modules/lambda"

  function_name = "seasons"

  filename = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.seasons"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}

module "episodes" {
  source = "./modules/lambda"

  function_name = "episodes"

  filename = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.episodes"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}

module "delete_show" {
  source = "./modules/lambda"

  function_name = "delete_show"

  filename = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handlers.delete_show"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}
