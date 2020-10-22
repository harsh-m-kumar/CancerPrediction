import boto3
import botocore

BUCKET_NAME = 'cancerpredictiondata' # replace with your bucket name
KEY1 = 'training_text.zip' #files in the S3 bucket
KEY2 = 'test_text.zip'
KEY3 = 'training_variants.zip'
KEY4= 'test_variants.zip'

a=[]
with open('rootkey.txt') as f:
    for line in f.readlines():
        a.append(line.split('=')[1])


s3 = boto3.resource('s3',aws_access_key_id=a[0][:-1],aws_secret_access_key=a[1])


s3.Bucket(BUCKET_NAME).download_file(KEY1, 'C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/training_text.zip')


s3.Bucket(BUCKET_NAME).download_file(KEY2, 'C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/test_text.zip')

s3.Bucket(BUCKET_NAME).download_file(KEY3, 'C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/training_variants.zip')


s3.Bucket(BUCKET_NAME).download_file(KEY4, 'C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/test_variants.zip')

