import os
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # 1. Initialize boto3 clients for CloudWatch and SNS
    # The billing metric is always stored in the us-east-1 region
    cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
    sns = boto3.client('sns')
    
    # Define threshold and notification targets
    THRESHOLD = 1.00
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:ap-south-1:135808938060:monitor-billing')
    
    print(f"Starting billing check. Threshold set to: ${THRESHOLD}")
    
    try:
        # 2. Retrieve the AWS billing metric from CloudWatch
        # Note: EstimatedCharges updates every few hours, so we check the last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=1)
        
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=21600,  # 6 hours
            Statistics=['Maximum']
        )
        
        datapoints = response.get('Datapoints', [])
        
        if not datapoints:
            print("No billing datapoints found in the specified timeframe.")
            return {
                'statusCode': 200,
                'body': 'No billing data available yet.'
            }
            
        # Get the latest maximum estimated charge
        # Sorting ensures we look at the most recent entry if multiple exist
        datapoints.sort(key=lambda x: x['Timestamp'])
        latest_charge = datapoints[-1]['Maximum']
        
        print(f"Current Estimated Charges: ${latest_charge:.2f}")
        
        # 3. Compare the billing amount with the threshold
        if latest_charge > THRESHOLD:
            print(f"Alert! Current charges (${latest_charge:.2f}) exceed threshold (${THRESHOLD:.2f}).")
            
            message = f"ALERT: Your AWS estimated monthly charges have reached ${latest_charge:.2f}, which exceeds your budget threshold of ${THRESHOLD:.2f}."
            subject = "AWS Billing Alert: Threshold Exceeded"
            
            # 4. If the billing exceeds the threshold, send an SNS notification
            sns_response = sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject=subject
            )
            
            # 5. Print messages for logging purposes
            print(f"SNS notification sent successfully. MessageId: {sns_response['MessageId']}")
        else:
            print(f"Billing is within limits. Charges (${latest_charge:.2f}) are below threshold (${THRESHOLD:.2f}).")
            
        return {
            'statusCode': 200,
            'body': f'Billing check complete. Current charge: ${latest_charge:.2f}'
        }
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error executing billing check: {str(e)}'
        }
