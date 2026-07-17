from common.repository import ShowRepository, SeasonRepository, EpisodeRepository
import pytest
import boto3

from moto import mock_aws

from .factories import ShowFactory, SeasonFactory


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
def show_repo(dynamodb_table):
    yield ShowRepository(dynamodb_table)


@pytest.fixture
def season_repo(dynamodb_table):
    yield SeasonRepository(dynamodb_table)


@pytest.fixture
def episode_repo(dynamodb_table):
    yield EpisodeRepository(dynamodb_table)


@pytest.fixture
def show(show_repo):
    item = ShowFactory.build()
    show_repo.put_show(item)
    yield item


@pytest.fixture
def seasons(season_repo, show):
    items = [SeasonFactory.build()]
    season_repo.put_seasons(show.name, items)
    yield items
