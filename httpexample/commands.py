import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import logging
import datetime
import os
import json
import random

settings = {
    'host': os.environ.get('ACCOUNT_HOST', ''),
    'master_key': os.environ.get('ACCOUNT_KEY', ''),
    'database_id': os.environ.get('COSMOS_DATABASE', 'SampleDB'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Persons'),
}

HOST = settings['host']
MASTER_KEY = settings['master_key']
DATABASE_ID = settings['database_id']
CONTAINER_ID = settings['container_id']


def get_container():
    client = cosmos_client.CosmosClient(
        HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)
    return container


def upsert_item(id, firstname, age):
    container = get_container()
    read_item = container.read_item(item=id, partition_key=firstname)
    item = {
        'id': read_item['id'],
        'firstname':read_item['firstname'],
        'age': age
    }
    response = container.replace_item(item=read_item, body=item)
    return response


def delete_item(id, firstname):
    container = get_container()
    container.delete_item(item=id, partition_key=firstname)

def get_all():
    container = get_container()
    return json.dumps(list(container.read_all_items(max_item_count=100)))


def create_item(firstname, age):
    container = get_container()
    item = {
        'id': str(random.randint(1, 1000)),
        'firstname': firstname,
        'age': age
    }
    container.create_item(body=item)
