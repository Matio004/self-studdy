module "lambda" {
  source = "./modules/lambda"

  for_each = local.handlers

  function_name = each.key
  filename      = data.archive_file.lambda_hello.output_path

  dynamo_actions = each.value.dynamo_actions

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

  dynamo_table_arn = aws_dynamodb_table.series_by_name.arn
  route_key        = each.value.route_key
}
