
locals {
  handlers = {
    get_show = {
      dynamo_actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem"
      ]
      route_key = "GET /shows/{name}"
    }

    get_seasons = {
      dynamo_actions = [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:PutItem",
        "dynamodb:BatchWriteItem"
      ]
      route_key = "GET /shows/{name}/seasons"
    }
    get_episodes = {
      dynamo_actions = [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:PutItem",
        "dynamodb:BatchWriteItem"

      ]
      route_key = "GET /shows/{name}/seasons/{season}"
    }
    delete_show = {
      dynamo_actions = [
        "dynamodb:Query",
        "dynamodb:DeleteItem",
        "dynamodb:BatchWriteItem"

      ]
      route_key = "DELETE /shows/{name}"
    }
    post_show = {
      dynamo_actions = [
        "dynamodb:PutItem"
      ]
      route_key = "POST /shows"
    }
    post_season = {
      dynamo_actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:BatchWriteItem"
      ]
      route_key = "POST /shows/{name}/seasons"
    }

    post_episode = {
      dynamo_actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:BatchWriteItem"
      ]
      route_key = "POST /shows/{name}/seasons/{season}"
    }
  }
}
