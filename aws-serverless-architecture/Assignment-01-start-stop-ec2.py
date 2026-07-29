import json
import boto3

# Initialize the EC2 client outside the handler to optimize container warm starts
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # 1. Define targets for the Stop action (Only target 'running' instances)
    stop_filters = [
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'tag:Action', 'Values': ['Auto-Stop']}
    ]
    
    # 2. Define targets for the Start action (Only target 'stopped' instances)
    start_filters = [
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'tag:Action', 'Values': ['Auto-start']}
    ]
    
    stopped_ids = []
    started_ids = []
    
    try:
        # ---- PROCESS AUTO-STOP ----
        stop_response = ec2.describe_instances(Filters=stop_filters)
        for reservation in stop_response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                stopped_ids.append(instance['InstanceId'])
                
        if stopped_ids:
            ec2.stop_instances(InstanceIds=stopped_ids)
            print(f"Successfully initiated stop for instances: {stopped_ids}")
        else:
            print("No running instances found with tag 'action=Auto-Stop'.")
            
        # ---- PROCESS AUTO-START ----
        start_response = ec2.describe_instances(Filters=start_filters)
        for reservation in start_response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                started_ids.append(instance['InstanceId'])
                
        if started_ids:
            ec2.start_instances(InstanceIds=started_ids)
            print(f"Successfully initiated start for instances: {started_ids}")
        else:
            print("No stopped instances found with tag 'action=Auto-start'.")
            
    except Exception as e:
        print(f"Error executing automation: {str(e)}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps({
            'StoppedInstances': stopped_ids,
            'StartedInstances': started_ids
        })
    }
