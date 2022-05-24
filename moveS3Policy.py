from urllib import response
import boto3 
client = boto3.client("s3")
s3 = boto3.resource("s3")
GUID = (input("Please Enter Customer GUID :") or "AJ4R2C6FGL1O5D0E").lower()
keyAlias = "key-"+GUID

client1 = boto3.client('kms')

response = client1.create_key(
    Tags=[{
        'TagKey': 'Alias',
        'TagValue': keyAlias
    }]
)

customer_key_id = response['KeyMetadata']['KeyId']
