import boto3
import os
import json
# Get the current working durectory
cwd = os.getcwd()

GUID = (input("Please Enter Customer GUID :") or "AJ4R2C6FGL1O5D0E").lower()
bucket_name = "customer-"+GUID+"-data"
# print(bucket_name)
s3 = boto3.resource('s3')

client = boto3.client("s3")
# function to check if bucket exists
def check_if_bucket_exist(bucketName):
    try:
        response = client.head_bucket(Bucket=bucketName)
        bucket_exist = True
    except Exception: 
        bucket_exist = False 
    
    if bucket_exist == True:
        return True
    else:
        return False    


# ############################# Do something if the bucket exist ###################################################
if check_if_bucket_exist(bucket_name):
    print("customer-" + GUID + "-data bucket exist")

    bucket = s3.Bucket(bucket_name)
    # delete all objects and bucket action
    bucket.objects.all().delete()
    bucket.object_versions.delete()
    bucket.delete()



    
s3.create_bucket(Bucket=bucket_name)

#**************************************  Add server acces logging begin *******************************************
policy_text = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ServerAccessLogsPolicy",
            "Effect": "Allow",
            "Principal": {
                "Service": "logging.s3.amazonaws.com"
            },
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::"+bucket_name+"/*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "900472373366"
                }
            }
        }
    ]
}			



def create_bucket_policy(policy, bucket_name):
    policy_string = json.dumps(policy)

    client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=policy_string
    )

create_bucket_policy(policy_text, bucket_name)  
def enable_server_access_logging(bucket_name, target_bucket, targeet_prefix):
    client.put_bucket_logging(
        Bucket=bucket_name,
        BucketLoggingStatus={
            'LoggingEnabled': {
                'TargetBucket': target_bucket,
                'TargetPrefix': targeet_prefix
            }
        }
    )

enable_server_access_logging(bucket_name, bucket_name, bucket_name+"-logs/")    

#************************************************* Add server acces logging end********************************   
# block public access
response = client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    },
    ExpectedBucketOwner='900472373366'
)

encrypt = client.put_bucket_encryption(
    Bucket=bucket_name,
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'aws:kms',
                    'KMSMasterKeyID': '42111eb0-4f30-439f-9495-0b8a7e8b30c2'
                },
                'BucketKeyEnabled': True
            }
        ]
    },
    ExpectedBucketOwner='900472373366'
)



# Expected bucket names
storage_bucket_name = "customer-"+GUID+"-storage"
landing_bucket_name = "customer-"+GUID+"-landing"
log_bucket_name = "customer-"+GUID+"-logging"

#Create director folders for data in custumer-data bucket
bucket.put_object(
    Body= '',
    Key= storage_bucket_name+'/'
)

bucket.put_object(
    Body= '',
    Key= landing_bucket_name+'/'
)

bucket.put_object(
    Body= '',
    Key= log_bucket_name+'/'
)

# Check if customer-GUID-landing bucket exist , then move objects and delete bucket
if check_if_bucket_exist(landing_bucket_name):
    landing_bucket = s3.Bucket(landing_bucket_name)

    # Move files from customer-xyz-storage-landing to data_bucket
    for s3_files in landing_bucket.objects.all():
        copy_source = {
            "Bucket": landing_bucket.name,
            "Key":  s3_files.key
        }
        print(copy_source)
        Key = landing_bucket.name+"/" + s3_files.key
        bucket.copy(copy_source, Key)
        print("A file is processed -->  " + s3_files.key)
    

    print("All files in customer-" + GUID + "-landing are copied to target bucket successfully")

    # getting an saving bucket policy####
    landing_result = client.get_bucket_policy(Bucket=landing_bucket_name)
    landing_policy = landing_result['Policy']

    # save policy in file
    f1 = open(landing_bucket_name+"-policy.txt", "w")
    f1.write(landing_policy)
    f1.close()

    # Move policy file to s3
    bucket.upload_file(cwd+"/"+landing_bucket_name+"-policy.txt", landing_bucket_name+"/"+landing_bucket_name+"-policy.txt")
    
    # delete objects and landing_bucket bucket
    landing_bucket.objects.all().delete()
    landing_bucket.object_versions.delete()
    landing_bucket.delete()
    print("customer-" + GUID + "-landing  bucket deleted successfully")
else:
    print("customer-" + GUID + "-landing bucket does not exist")   


# Check if customer-GUID-storage bucket exist , then move objects and delete bucket
if check_if_bucket_exist(storage_bucket_name):
    storge_bucket = s3.Bucket(storage_bucket_name)
    # Move files from customer-GUID-storage to bucket
    for s3_files in storge_bucket.objects.all():
        copy_source = {
            "Bucket": storge_bucket.name,
            "Key":  s3_files.key
        }
        print(copy_source)
        Key = storge_bucket.name+"/" + s3_files.key
        bucket.copy(copy_source, Key)
        print("A file is processed -->  " + s3_files.key)
    

    print("All files in customer-" + GUID + "-storage are copied to target bucket successfully")

    # getting an savin bucket policy####
    storage_result = client.get_bucket_policy(Bucket=storage_bucket_name)
    storage_policy = storage_result['Policy']


    # save policy in file
    f2 = open(storage_bucket_name+"-policy.txt", "w")
    f2.write(storage_policy)
    f2.close()

    # Move policy file to s3
    bucket.upload_file(cwd+"/"+storage_bucket_name+"-policy.txt", storage_bucket_name+"/"+storage_bucket_name+"-policy.txt")        

    # delete objects and storge_bucket bucket
    storge_bucket.objects.all().delete()
    storge_bucket.object_versions.delete()
    storge_bucket.delete()
    print("customer-" + GUID + "-storage bucket deleted successfully")
else:
    print("customer-" + GUID + "-storage bucket does not exist") 

    

# Check if customer-GUID-logging bucket exist , then move objects and delete bucket
if check_if_bucket_exist(log_bucket_name):
    log_bucket = s3.Bucket(log_bucket_name)
    # Move files from customer-GUID-logs to data bucket
    for s3_files in log_bucket.objects.all():
        copy_source = {
            "Bucket": log_bucket.name,
            "Key":  s3_files.key
        }
        print(copy_source)
        Key = log_bucket.name+"/" + s3_files.key
        bucket.copy(copy_source, Key)
        print("A file is processed -->  " + s3_files.key)
        

    print("All files in customer-" + GUID + "-logging are copied to target bucket successfully")

    # getting and saving bucket policy####
    logging_result = client.get_bucket_policy(Bucket=log_bucket_name)
    logging_policy = logging_result['Policy']   

    # create file and add policy
    f3 = open(log_bucket_name+"-policy.txt", "w")
    f3.write(logging_policy)
    f3.close()

    # Move policy file to s3
    bucket.upload_file(cwd+"/"+log_bucket_name+"-policy.txt", log_bucket_name+"/"+log_bucket_name+"-policy.txt")

    # delete objects and log_bucket bucket
    log_bucket.objects.all().delete()
    log_bucket.object_versions.delete()
    log_bucket.delete()
    print("customer-" + GUID + "-logging bucket deleted successfully")
else:
    print("customer-" + GUID + "-logging bucket does not exist")    
        
        


   
