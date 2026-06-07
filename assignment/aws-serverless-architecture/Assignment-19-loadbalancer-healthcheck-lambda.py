import json
import boto3
from datetime import datetime

elbv2 = boto3.client('elbv2')
sns = boto3.client('sns')

ALB_ARN = "arn:aws:elasticloadbalancing:ap-south-1:135808938060:loadbalancer/app/ftg-lb/f9c180112d3b5945"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:135808938060:loadbalancer-healthcheck-topic"

def lambda_handler(event, context):

    unhealthy_targets = []

    try:
        # Get all target groups attached to ALB
        target_groups = elbv2.describe_target_groups(
            LoadBalancerArn=ALB_ARN
        )['TargetGroups']

        for tg in target_groups:

            tg_name = tg['TargetGroupName']
            tg_arn = tg['TargetGroupArn']

            target_health = elbv2.describe_target_health(
                TargetGroupArn=tg_arn
            )

            for target in target_health['TargetHealthDescriptions']:

                target_id = target['Target']['Id']
                target_port = target['Target']['Port']

                state = target['TargetHealth']['State']
                reason = target['TargetHealth'].get('Reason', 'N/A')
                description = target['TargetHealth'].get('Description', 'N/A')

                if state != 'healthy':
                    unhealthy_targets.append({
                        "TargetGroup": tg_name,
                        "InstanceId": target_id,
                        "Port": target_port,
                        "State": state,
                        "Reason": reason,
                        "Description": description
                    })

        if unhealthy_targets:

            message = {
                "Timestamp": datetime.utcnow().isoformat(),
                "LoadBalancerArn": ALB_ARN,
                "UnhealthyTargets": unhealthy_targets
            }

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="ALB Health Check Alert - Unhealthy Targets Detected",
                Message=json.dumps(message, indent=4)
            )

            return {
                "statusCode": 200,
                "message": f"{len(unhealthy_targets)} unhealthy targets found and SNS notification sent."
            }

        return {
            "statusCode": 200,
            "message": "All targets are healthy."
        }

    except Exception as e:
        print(f"Error: {str(e)}")

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="ALB Health Check Lambda Error",
            Message=str(e)
        )

        raise