import boto3
import os
from datetime import datetime, timedelta, timezone

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

# Environment Variables
REGION = ['ap-south-1']
LOAD_BALANCER_NAME = os.environ['app/ftg-lb/f9c180112d3b5945']
SNS_TOPIC_ARN = os.environ['arn:aws:sns:ap-south-1:135808938060:auto-scale-topic']
AMI_ID = os.environ['ami-067c93806d6624f41']
INSTANCE_TYPE = os.environ.get('INSTANCE_TYPE', 't3.micro')
KEY_NAME = os.environ['ftgkey']
SECURITY_GROUP_ID = os.environ['sg-00cd4cadf40faf3cf']
SUBNET_ID = os.environ['subnet-074685289d0a53e5c']

HIGH_THRESHOLD = 0.8
LOW_THRESHOLD = 0.9


def get_load_metric():
    """
    Get average RequestCount metric for the last 5 minutes.
    You can replace this with other metrics such as
    TargetResponseTime, HealthyHostCount, etc.
    """

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=5)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='RequestCount',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': LOAD_BALANCER_NAME
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=120,
        Statistics=['Average']
    )

    datapoints = response.get('Datapoints', [])

    if not datapoints:
        return 0

    return datapoints[0]['Average']


def get_running_instances():
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
            {
                'Name': 'tag:AutoManaged',
                'Values': ['true']
            }
        ]
    )

    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    return instances


def launch_instance():

    response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        MinCount=1,
        MaxCount=1,
        KeyName=KEY_NAME,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        SubnetId=SUBNET_ID,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'AutoManaged',
                        'Value': 'true'
                    }
                ]
            }
        ]
    )

    instance_id = response['Instances'][0]['InstanceId']

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='Scale Out Action',
        Message=f'New EC2 instance launched: {instance_id}'
    )

    return instance_id


def terminate_instance():

    instances = get_running_instances()

    if len(instances) <= 1:
        print("Minimum instance count reached.")
        return None

    instance_id = instances[-1]

    ec2.terminate_instances(
        InstanceIds=[instance_id]
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='Scale In Action',
        Message=f'EC2 instance terminated: {instance_id}'
    )

    return instance_id


def lambda_handler(event, context):

    load = get_load_metric()

    print(f"Current Load Metric: {load}")

    if load > HIGH_THRESHOLD:

        instance_id = launch_instance()

        return {
            'statusCode': 200,
            'action': 'scale-out',
            'instance_id': instance_id,
            'load': load
        }

    elif load < LOW_THRESHOLD:

        instance_id = terminate_instance()

        return {
            'statusCode': 200,
            'action': 'scale-in',
            'instance_id': instance_id,
            'load': load
        }

    else:

        return {
            'statusCode': 200,
            'action': 'none',
            'load': load
        }