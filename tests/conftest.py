from repository import ShowRepository, SeasonRepository, EpisodeRepository
import pytest
import boto3

from moto import mock_aws

from factories import ShowFactory


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="services_by_name",
            KeySchema=[
                {"AttributeName": "name", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "name", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table


@pytest.fixture
def show(dynamodb_table):
    item = ShowFactory.build()
    dynamodb_table.put_item(
        Item={"name": item.name, "sk": "SHOW", "data": item.model_dump(mode="json")}
    )
    yield item
    dynamodb_table.delete_item(Key={"name": item.name, "sk": "SHOW"})


@pytest.fixture
def seasons(dynamodb_table):
    pass


@pytest.fixture
def show_repo(dynamodb_table):
    yield ShowRepository(dynamodb_table)


@pytest.fixture
def season_repo(dynamodb_table):
    yield SeasonRepository(dynamodb_table)


@pytest.fixture
def episode_repo(dynamodb_table):
    yield EpisodeRepository(dynamodb_table)
