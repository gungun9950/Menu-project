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

def stop_ec2_instance(instance_id, aws_access_key_id, aws_secret_access_key, region_name):
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        response = ec2.stop_instances(InstanceIds=[instance_id])
        return response
    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}

try:
    # Read and parse incoming POST data
    post_data = json.load(sys.stdin)

    instance_id = post_data.get('instanceId')
    aws_access_key_id = post_data.get('awsAccessKeyId')
    aws_secret_access_key = post_data.get('awsSecretAccessKey')
    region_name = post_data.get('regionName')

    if instance_id and aws_access_key_id and aws_secret_access_key and region_name:
        result = stop_ec2_instance(instance_id, aws_access_key_id, aws_secret_access_key, region_name)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing required parameters."}))
except Exception as e:
    print(json.dumps({"error": "An unexpected error occurred: " + str(e)}))
[root@ip-172-31-39-253 cgi-bin]# cat
^C
[root@ip-172-31-39-253 cgi-bin]# cat create_cloudformation_stack.py
#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3

# Enable CGI traceback for debugging
cgitb.enable()

def create_cloudformation_stack(stack_name, template_url, aws_access_key_id, aws_secret_access_key, region_name):
    try:
        cloudformation = boto3.client(
            'cloudformation',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        response = cloudformation.create_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_NAMED_IAM']  # Add more capabilities as needed
        )
        return response
    except Exception as e:
        return {"error": str(e)}

print("Content-Type: application/json\n")

try:
    input_data = cgi.FieldStorage()
    raw_data = input_data.file.read()  # Read the input data as bytes
    post_data = json.loads(raw_data.decode('utf-8'))  # Decode bytes to str and then load JSON

    stack_name = post_data.get('stackName')
    template_url = post_data.get('templateURL')
    aws_access_key_id = post_data.get('awsAccessKeyId')
    aws_secret_access_key = post_data.get('awsSecretAccessKey')
    region_name = post_data.get('regionName')

    if all([stack_name, template_url, aws_access_key_id, aws_secret_access_key, region_name]):
        result = create_cloudformation_stack(stack_name, template_url, aws_access_key_id, aws_secret_access_key, region_name)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Missing required parameters."}))
except Exception as e:
    print(json.dumps({"error": "An unexpected error occurred: " + str(e)}))
