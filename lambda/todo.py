from __future__ import print_function  # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import logging
import os
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: " + event["httpMethod"])
    verbs = {
        "DELETE": delete,
        "GET": get,
        "POST": post,
        "PUT": put,
        "OPTIONS": options
    }
    return verbs[event["httpMethod"]](event, context)


def delete(event, context):

    try:
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        table.delete_item(
            Key={
                'todo_id': event['queryStringParameters']['todo_id']
            }
        )
        response = {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            }
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response


def get(event, context):
    return scan()


def getItem(todo):
    try:
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        result_todo = table.get_item(
            Key={
                'todo_id': todo['todo']['todo_id']
            }
        )
        response = {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "body": json.dumps(result_todo["Item"])
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response


def scan():
    try:
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        items = table.scan()
        response = {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "body": json.dumps(items["Items"])
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response


def post(event, context):
    logger.info("Received event: " + json.dumps(json.loads(event["body"]), indent=2))
    try:
        todo = json.loads(event["body"])
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        todo['todo']['todo_id'] = str(uuid.uuid4())
        table.put_item(
            Item=todo['todo']
        )
        result_todo = table.get_item(
            Key={
                'todo_id': todo['todo']['todo_id']
            }
        )
        response = {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "body": json.dumps(result_todo["Item"])
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response


def put(event, context):
    logger.info("Received event: " + json.dumps(json.loads(event["body"]), indent=2))
    try:
        todo = json.loads(event["body"])
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        table.update_item(
            Key={
                'todo_id': todo['todo']['todo_id']
            },
            UpdateExpression="set task = :task",
            ExpressionAttributeValues={
                ':task': todo['todo']['task']
            },
            ReturnValues="UPDATED_NEW"
        )
        result_todo = table.get_item(
            Key={
                'todo_id': todo['todo']['todo_id']
            }
        )
        response = {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "body": json.dumps(result_todo["Item"])
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "headers": {
                'Access-Control-Allow-Origin': os.environ['CORS'],
                'Content-Type': 'application/json'
            },
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response


def options(event, context):
    response = {
        "statusCode": "200",
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
            'Access-Control-Allow-Origin': os.environ['CORS'],
            'Access-Control-Allow-Methods': 'DELETE,GET,POST,PUT,OPTIONS'
        }
    }
    return response
