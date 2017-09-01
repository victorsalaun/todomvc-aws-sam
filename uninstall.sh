#!/usr/bin/env bash

DIGITS_RE='^[0-9]+$'
TEMPLATE_FILE_NAME='todomvc.cfn.yml'
PACKAGE_FILE_NAME='todomvc-xfm.cfn.yml'
STACK_NAME='TodoApp'

# Check if the aws cli is installed
if ! command -v aws > /dev/null; then
    echo "aws cli was not found. Please install before running this script."
    exit 1
fi

ACCOUNT_ID=`aws iam get-user | grep 'arn:aws:iam' | tr -dc '0-9'`
BUCKET_NAME="todomvc-aws-sam-s3"
REGION=`aws configure get region`

# Try to remove the package
if aws cloudformation delete-stack --stack-name ${STACK_NAME}; then
    echo "Package ${STACK_NAME} removed successfully"
else
    echo "Failed removing package ${STACK_NAME}"
    exit 1
fi

# Try to remove the bucket
if aws s3 rb s3://${BUCKET_NAME}; then
    echo "Bucket s3://${BUCKET_NAME} removed successfully"
else
    echo "Failed removing bucket s3://${BUCKET_NAME}"
    exit 1
fi