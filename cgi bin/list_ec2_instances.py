#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys

# Enable CGI traceback for debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: application/json\n")

def list_ec2_instances(aws_access_key_id, aws_secret_access_key, region_name):
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'LaunchTime': instance['LaunchTime'].isoformat()
                })
        return instances
    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}

try:
    # Read and parse incoming POST data
    post_data = json.load(sys.stdin)

    aws_access_key_id = post_data.get('awsAccessKeyId')
    aws_secret_access_key = post_data.get('awsSecretAccessKey')
    region_name = post_data.get('regionName')

    if aws_access_key_id and aws_secret_access_key and region_name:
        result = list_ec2_instances(aws_access_key_id, aws_secret_access_key, region_name)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing required parameters."}))
except Exception as e:
    print(json.dumps({"error": "An unexpected error occurred: " + str(e)}))
