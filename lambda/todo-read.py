from __future__ import print_function  # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if 'resourceId' in event:
        return getItem(event['pathParameters']['resourceId'])
    else:
        return scan()


def getItem(id):
    try:
        table_name = os.environ['TABLE_NAME']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        result_todo = table.get_item(
            Key={
                'todo_id': id
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
