import boto3   
GUID = (input("Please Enter Customer GUID :") or "AJ4R2C6FGL1O5D0E").lower()
bucket_name = "customer-" + GUID + "-data "
s3 = boto3.resource('s3')
# Bucket names 
Landing_bucket = "customer-" + GUID + "-landing"
Storage_bucket = "customer-" + GUID + "-storage"
Logging_bucket = "customer-" + GUID + "-logging"
Data_bucket = "customer-" + GUID + "-data"


# Getting buckets to transfer files
storge_bucket = s3.Bucket("customer-"+GUID+"-storage")
landing_bucket = s3.Bucket("customer-"+GUID+"-landing")
log_bucket = s3.Bucket("customer-"+GUID+"-logging")



# s3.create_bucket(Bucket=Landing_bucket)
# s3.create_bucket(Bucket=Storage_bucket)
# s3.create_bucket(Bucket=Logging_bucket)
# s3.create_bucket(Bucket=Data_bucket)


# Deleting buckets
# delete objects and storge_bucket bucket
storge_bucket.objects.all().delete()
storge_bucket.object_versions.delete()
storge_bucket.delete()

# delete objects and log_bucket bucket
log_bucket.objects.all().delete()
log_bucket.object_versions.delete()
log_bucket.delete()

# delete objects and landing_bucket bucket
landing_bucket.objects.all().delete()
landing_bucket.object_versions.delete()
landing_bucket.delete()
