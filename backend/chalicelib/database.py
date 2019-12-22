import os
import uuid

import boto3
from boto3.dynamodb.conditions import Key


def _get_database():
    endpoint = os.environ.get('DB_ENDPOINT')
    if endpoint:
        return boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        return boto3.resource('dynamodb')


def get_all_todos():
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.scan()
    return response['Items']


def get_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.query(
        KeyConditionExpression=Key('id').eq(todo_id)
    )
    items = response['Items']
    return items[0] if items else None


def create_todo(todo):
    item = {
        'id': uuid.uuid4().hex,
        'title': todo['title'],
        'memo': todo['memo'],
        'priority': todo['priority'],
        'completed': False,
    }

    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    table.put_item(Item=item)
    return item


def update_todo(todo_id, changes):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    update_expression = []
    expression_attribute_values = {}
    for key in ['title', 'memo', 'priority', 'completed']:
        if key in changes:
            update_expression.append(f"{key} = :{key[0:1]}")
            expression_attribute_values[f":{key[0:1]}"] = changes[key]

    result = table.update_item(
        Key={
            'id': todo_id,
        },
        UpdateExpression='set ' + ','.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']


def delete_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    result = table.delete_item(
        Key={
            'id': todo_id,
        },
        ReturnValues='ALL_OLD'
    )
    return result['Attributes']


def broadcast_gaora(memo):
    if len(memo) > 30:
        memo = "ホームラン" + memo
    if "ホームラン" in memo:
        memo = memo.replace("ホームラン", "『イッツ！』")
        memo += "『ゴーンヌ!』"
    return memo
