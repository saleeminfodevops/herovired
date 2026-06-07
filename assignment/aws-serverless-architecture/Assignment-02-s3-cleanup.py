import boto3
import os
from datetime import datetime, timedelta, timezone

# Initialize S3 Client
s3_client = boto3.client('s3', region_name='ap-south-1')

def lambda_handler(event, context):
    # Retrieve the bucket name from environment variables
    bucket_name = os.environ.get('ftg-s3-01 ')
    if not bucket_name:
        return {"status": "error", "message": "Environment variable 'ftg-s3-01 ' is missing."}
        
    # Calculate threshold date (30 days ago, making it timezone aware)
    days_threshold = 10
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    
    # Initialize pagination parameters
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)
    
    deleted_count = 0
    objects_to_delete = []

    print(f"Scanning bucket '{bucket_name}' for files older than {cutoff_date}...")

    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            # Compare LastModified timestamp
            if obj['LastModified'] < cutoff_date:
                objects_to_delete.append({'Key': obj['Key']})
                
                # S3 delete_objects API takes a maximum of 1,000 objects per request
                if len(objects_to_delete) == 1000:
                    response = s3_client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': objects_to_delete}
                    )
                    deleted_count += len(response.get('Deleted', []))
                    objects_to_delete = []  # Reset batch array

    # Delete any remaining objects under the 1,000 count limit
    if objects_to_delete:
        response = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )
        deleted_count += len(response.get('Deleted', []))

    print(f"Cleanup finished. Successfully deleted {deleted_count} objects.")
    return {
        "status": "success",
        "deleted_objects_count": deleted_count
    }