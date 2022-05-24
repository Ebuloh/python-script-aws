import os
import json
import boto3
import os
s3 = boto3.resource('s3')
cwd = os.getcwd()
client = boto3.client("s3")


GUID = (input("Please Enter Customer GUID :") or "AJ4R2C6FGL1O5D0E").lower()
data_bucket_name = "customer-"+GUID+"-data"

# Bucket names 
Landing_bucket_name = "customer-" + GUID + "-landing"
Storage_bucket_name = "customer-" + GUID + "-storage"
Logging_bucket_name = "customer-" + GUID + "-logging"

#buckets
landing_bucket = s3.Bucket(Landing_bucket_name)


def create_bucket_policy(policy, bucket_name):
    policy_string = json.dumps(policy)

    client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=policy_string
    )

data_bucket = s3.Bucket(data_bucket_name)

# ########## Move all objects from data_bucket to respective buckets ############

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

move_object_policy_to_bucket(Landing_bucket_name, "landing")  
move_object_policy_to_bucket(Logging_bucket_name, "logging")    
move_object_policy_to_bucket(Storage_bucket_name, "storage")            



# ########## Move all objects from data_bucket to logging_bucket  ############

# for object in data_bucket.objects.all().filter(Prefix="customer-aj4r2c6fgl1o5d0e-landing/"):
#     if object.key == "customer-aj4r2c6fgl1o5d0e-landing/customer-aj4r2c6fgl1o5d0e-landing-policy.txt":
#         data_bucket.download_file(object.key, cwd+"/landing-policy.txt")
#         f1 = open("landing-policy.txt", "r")
#         policy1 = json.loads(f1.read())
#         print(policy1)
#         f1.close()
#         create_bucket_policy(policy1, Landing_bucket_name)

#     print(object.key)
#     if object.key != "customer-aj4r2c6fgl1o5d0e-landing/":
#         copy_source = {
#             "Bucket": data_bucket.name,
#             "Key":  object.key
#         }
#         print(copy_source)
#         Key = (object.key).replace('customer-aj4r2c6fgl1o5d0e-landing/', '')
#         landing_bucket.copy(copy_source, Key)
#         print("A file is processed -->  " + object.key) 

