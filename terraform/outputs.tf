output "api_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "lambda_functions" {
  value = {
    for name, module_instance in module.lambda :
    name => module_instance.function_name
  }

}

output "common_layer_name" {
  value = aws_lambda_layer_version.common.layer_name
}

output "dependencies_layer_name" {
  value = aws_lambda_layer_version.python_dependencies.layer_name
}
