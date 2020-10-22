import boto3
from botocore.client import Config

ACCESS_KEY_ID = '**********************'
ACCESS_SECRET_KEY = '********************'
BUCKET_NAME = '*********************'

data1 = open('Data/training_text.zip', 'rb')
data2=open('Data/test_text.zip','rb')
data3=open('Data/training_variants.zip','rb')
data4=open('Data/test_variants.zip','rb')


s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key='training_text.zip', Body=data1)
s3.Bucket(BUCKET_NAME).put_object(Key='test_text.zip',Body=data2)
s3.Bucket(BUCKET_NAME).put_object(Key='training_variants.zip',Body=data3)
s3.Bucket(BUCKET_NAME).put_object(Key='test_variants.zip',Body=data4)

s3.Bucket()
print ("Done")
