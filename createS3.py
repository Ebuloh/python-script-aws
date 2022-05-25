import boto3   
import json
import os
GUID = (input("Please Enter Customer GUID :") or "AJ4R2C6FGL1O5D0E").lower()
s3 = boto3.resource('s3')
client = boto3.client("s3")
cwd = os.getcwd()
client1 = boto3.client('kms')



# Bucket names 
Landing_bucket = "customer-" + GUID + "-landing"
Storage_bucket = "customer-" + GUID + "-storage"
Logging_bucket = "customer-" + GUID + "-logging"
Data_bucket = "customer-" + GUID + "-data"


# creating buckets
s3.create_bucket(Bucket=Landing_bucket)
s3.create_bucket(Bucket=Storage_bucket)
s3.create_bucket(Bucket=Logging_bucket)

# #add basic bucket policy
L_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSSLRequestsOnly_nkjpnk",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::"+Landing_bucket,
                "arn:aws:s3:::"+Landing_bucket+"/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}

Lo_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSSLRequestsOnly_nkjpnk",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::"+Logging_bucket,
                "arn:aws:s3:::"+Logging_bucket+"/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}

S_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSSLRequestsOnly_nkjpnk",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::"+Storage_bucket,
                "arn:aws:s3:::"+Storage_bucket+"/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
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

create_bucket_policy(L_policy, Landing_bucket)
create_bucket_policy(Lo_policy, Logging_bucket)
create_bucket_policy(S_policy, Storage_bucket)

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

#*********************************** Enable server access logging start**********************************************
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
            "Resource": "arn:aws:s3:::"+Logging_bucket+"/*",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": "900472373366"
                }
            }
        }
    ]
}			

# bucket_policy = s3.BucketPolicy(Logging_bucket)

# response = bucket_policy.put(
#     Policy = policy,
#     ExpectedBucketOwner= "900472373366"
# )

create_bucket_policy(policy_text, Logging_bucket)  
#***************************** Enable server access logging end****************************************************


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

enable_server_access_logging(Landing_bucket, Logging_bucket, Landing_bucket+"-logs/" )   
enable_server_access_logging(Logging_bucket, Logging_bucket, Logging_bucket+"-logs/" )   
enable_server_access_logging(Storage_bucket, Logging_bucket, Storage_bucket+"-logs/" )   

# block public access landing bucket
response = client.put_public_access_block(
    Bucket=Landing_bucket,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    },
    ExpectedBucketOwner='900472373366'
)

# block public access Logging bucket
response = client.put_public_access_block(
    Bucket=Logging_bucket,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    },
    ExpectedBucketOwner='900472373366'
)

# block public access storage bucket
response = client.put_public_access_block(
    Bucket=Storage_bucket,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    },
    ExpectedBucketOwner='900472373366'
)


# function to get bucket encryption
def get_bucket_encryption_key(bucketName, account):
    response = client.get_bucket_encryption(
        Bucket=bucketName,
        ExpectedBucketOwner=account
    )

    return response["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["KMSMasterKeyID"]

if check_if_bucket_exist(Data_bucket):
    encryption_key = get_bucket_encryption_key(Data_bucket, "900472373366")

    # Encrypting Landing_bucket
    encrypt = client.put_bucket_encryption(
        Bucket=Landing_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': encryption_key
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )  

    # Encrypting Logging_bucket
    encrypt1 = client.put_bucket_encryption(
        Bucket=Logging_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': encryption_key
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )   

    # encryyypting Storage_bucket
    encrypt2 = client.put_bucket_encryption(
        Bucket=Storage_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': encryption_key
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )     

    

    # ########## Move all objects from data_bucket to respective buckets ############
    data_bucket = s3.Bucket(Data_bucket)

    def move_object_policy_to_bucket(bucketName, bucketSuffix):
        bucket_to = s3.Bucket(bucketName)

        for object in data_bucket.objects.all().filter(Prefix=bucketName+"/"):
            if object.key == bucketName+"/"+bucketName+"-policy.txt":
                data_bucket.download_file(object.key, cwd+"/"+bucketSuffix+"-policy.txt")
                f1 = open(bucketSuffix+"-policy.txt", "r")
                policy1 = json.loads(f1.read())
                print(policy1)
                f1.close()
                create_bucket_policy(policy1, bucketName)

            if object.key != bucketName+"/":
                copy_source = {
                    "Bucket": data_bucket.name,
                    "Key":  object.key
                }
                print(copy_source)
                Key = (object.key).replace(bucketName+'/', '')
                bucket_to.copy(copy_source, Key)
                print("A file is processed -->  " + object.key) 

    move_object_policy_to_bucket(Landing_bucket, "landing")  
    move_object_policy_to_bucket(Logging_bucket, "logging")    
    move_object_policy_to_bucket(Storage_bucket, "storage")       


else:
    print(Data_bucket + " does not exist")
    keyAlias = "alias/key-"+GUID

    response = client1.create_key(
        Tags=[{
            'TagKey': 'Alias',
            'TagValue': keyAlias
        }]
    )

    customer_key_id = response['KeyMetadata']['KeyId']

    response1 = client1.create_alias(
        AliasName=keyAlias,
        TargettKeyId=customer_key_id
    )
    
    # Encrypting Landing_bucket
    encrypt = client.put_bucket_encryption(
        Bucket=Landing_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': customer_key_id
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )  

    # Encrypting Logging_bucket
    encrypt1 = client.put_bucket_encryption(
        Bucket=Logging_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': customer_key_id
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )

    # encryyypting Storage_bucket
    encrypt2 = client.put_bucket_encryption(
        Bucket=Storage_bucket,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': customer_key_id
                    },
                    'BucketKeyEnabled': True
                }
            ]
        },
        ExpectedBucketOwner='900472373366'
    )            

