import boto3
ec2 = boto3.resource('ec2')

keyPair = input("Please enter the key name: ") or "fritz_key"
subnet = input("Please enter the subnet ID: ") or "subnet-0bdf3709e9c25d6d9"
serviceType = input("Please enter the service type for honytrap: ") or "smtp"
instance_name = input("Please enter the iinstance name: ") or "h-mail"

instance = ec2.create_instances(
    ImageId='ami-03093518a419d5cd8',
    InstanceType='t2.micro',
    KeyName=keyPair,
    MaxCount=1,
    MinCount=1,
    SecurityGroupIds=[
        'sg-068d3577daeec4c26',
    ],
    SubnetId=subnet,
    UserData='''#!/bin/bash
      yum update -y
      service docker start
      sudo docker run -p 8080:25 honeytrap/smtp''',

   
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
                {
                    'Key': 'service type',
                    'Value': serviceType
                }
            ]
        },
    ],


)