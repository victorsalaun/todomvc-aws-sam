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
