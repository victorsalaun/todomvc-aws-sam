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
            "body": json.dumps(result_todo["Item"])
        }
        return response
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        response = {
            "statusCode": "400",
            "message": json.dumps(e.response['Error']['Message'])
        }
        return response
