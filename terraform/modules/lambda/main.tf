resource "aws_lambda_function" "this" {
  function_name = var.function_name

  filename         = var.filename
  source_code_hash = base64sha256(var.filename)

  role    = aws_iam_role.this.arn
  handler = var.handler
  runtime = var.runtime

  layers = var.layers

  environment {
    variables = var.enviroment_variables
  }
}

resource "aws_apigatewayv2_integration" "this" {
  api_id                 = var.api_gateway_id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.this.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${var.api_gateway_execution_arn}/*/*"
}

# iam role
resource "aws_iam_role" "this" {
  name = "${var.function_name}_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# log policy
resource "aws_iam_role_policy_attachment" "this" {
  role = aws_iam_role.this.name
  # arn:<partition>:<service>:<region>:<account_id>:<resource>
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "this" {
  name = "${var.function_name}-lambda-dynamodb-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = var.dynamo_actions
        Resource = var.dynamo_table_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "this_ddb" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}
