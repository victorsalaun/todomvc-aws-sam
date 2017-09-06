'use strict';

const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();

const tableName = process.env.TABLE_NAME;

const createResponse = (statusCode, body) => {
    return {
        statusCode: statusCode,
        body: JSON.stringify(body)
    }
};

exports.lambda_handler = (event, context, callback) => {

    let params = {};
    if (event.pathParameters.resourceId !== null) {
        params = {
            TableName: tableName,
            Key: {
                todo_id: event.pathParameters.resourceId
            }
        };
    } else {
        params = {
            TableName: tableName
        };
    }

    let dbGet = (params) => {
        return dynamo.get(params).promise()
    };

    dbGet(params).then((data) => {
        if (!data.Item) {
            callback(null, createResponse(404, "ITEM NOT FOUND"));
            return;
        }
        console.log(`RETRIEVED ITEM SUCCESSFULLY WITH doc = ${data.Item}`);
        callback(null, createResponse(200, data.Item));
    }).catch((err) => {
        console.log(`GET ITEM FAILED FOR doc = ${params.Key.id}, WITH ERROR: ${err}`);
        callback(null, createResponse(500, err));
    });
};