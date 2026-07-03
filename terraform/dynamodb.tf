resource "aws_dynamodb_table" "series_by_name" {
  name         = "series_by_name"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "name" # todo partition key

  attribute {
    name = "name"
    type = "S"
  }

}