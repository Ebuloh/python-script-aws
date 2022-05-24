import boto3 
import datetime
#bucket name
bucket_name = "mail.vctrzr.com"
#folder name 
# folder_name = ""
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
# def handler(event, context):
#     for file in bucket.objects:
#         if (file.last_modified).replace(tzinfo = None) > datetime.datetime(2022, 5, 8, tzinfo = None):
#            # Print results
#            print('File Name: %s ---- Date: %s' % (file.key, file.last_modified))

data = bucket.objects.all()
for item in data:
    print(item)