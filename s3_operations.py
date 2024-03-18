import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Get the S3 bucket name from environment variable
S3_BUCKET = os.getenv('S3_BUCKET')

# Function to upload file to S3
def upload_file(title):
    filepath = f'../yt-Videos/{title}'
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        return False

    # Upload the file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(filepath, S3_BUCKET, title)
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
    # print("Finished uploading file to S3")
    return True
