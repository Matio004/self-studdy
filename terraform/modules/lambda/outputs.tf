output "function_name" {
  value = aws_lambda_function.this.function_name
}

output "integration_id" {
  value = aws_apigatewayv2_integration.this.id
}
