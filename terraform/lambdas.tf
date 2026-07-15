module "hello" {
  source = "./modules/lambda"

  function_name = "get_show"
  filename      = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}

module "seasons" {
  source = "./modules/lambda"

  function_name = "get_seasons"

  filename = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}

module "episodes" {
  source = "./modules/lambda"

  function_name = "get_episodes"

  filename = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
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
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}
module "create_show" {
  source = "./modules/lambda"

  function_name = "post_show"
  filename      = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}


module "create_season" {
  source = "./modules/lambda"

  function_name = "post_season"
  filename      = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}


module "create_episode" {
  source = "./modules/lambda"

  function_name = "post_episode"
  filename      = data.archive_file.lambda_hello.output_path

  role    = aws_iam_role.lambda_role.arn
  handler = "handler.lambda_handler"
  runtime = "python3.12"

  layers = [
    aws_lambda_layer_version.python_dependencies.arn,
    aws_lambda_layer_version.common.arn
  ]

  enviroment_variables = {
    TABLE_NAME = aws_dynamodb_table.series_by_name.name
  }

  api_gateway_id            = aws_apigatewayv2_api.api.id
  api_gateway_execution_arn = aws_apigatewayv2_api.api.execution_arn
}


