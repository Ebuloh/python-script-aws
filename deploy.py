import boto3
sess = boto3.Session(region_name = 'us-east-1')
cfnClient = sess.client('cloudformation')

### Input parameters.
VpcCIDR = input("Please enter the VPC CIDR for your VPC: ") or "10.0.0.0/16"
VPCNAME = input("Please enter your VPC name: ") or "client vpc name"
ClientSubCidr = input("Please Enter the CIDR for the client subnet: ") or "10.0.0.0/24"
AppSubCidr = input("Please enter the CIDR for the app subnet: ") or "10.0.1.0/24"
LambdaSubCidr = input("Please enter the CIDR for the Lambda subnet: ") or "10.0.2.0/24"
EndpointCidrBlock = input("Please enter the VPN Enpoint CidrBlock: ") or "192.169.0.0/16"
EndpointServerCert = input("Please enter the server certificate: ") or "arn:aws:acm:us-east-1:900472373366:certificate/4f1d0f27-00ba-4472-8ec7-4e0bc1054ff7"
ClientServerCert = input("Please enter the Client Certificate: ") or "arn:aws:acm:us-east-1:900472373366:certificate/32ebc0d7-d716-4ec1-8134-1c83a88d606b"
S3Bucket1Name = input("Please enter the first S3 bucket name: ") or "customer2-simple-storagetest"
S3Bucket2Name = input("Please enter the second S3 bucket name: ") or "customer2-simple-storage-landingtest"                 
Customer2AppServerInstanceType = input("Please enter the app instance type: ") or "t2.micro"
Customer2AppServerKeyName = input("Please enter the key for the app instance: ") or "VZdarren-vzt"
Customer2AppServerImageId = input("Please enter the Image ID  for the app instance: ") or "ami-0c02fb55956c7d316"
Customer2AppServerSubnetId = input("Please enter the subnet ID for the app : ") or "subnet-02dc4768137dd8b40"
Customer2AppServerSecurityGroup = input("Please enter the security group for the app instance: ") or "sg-0d118715dbaeec5a4"
Customer1KMSKeyArn = input("Please enter the customer1KMSArn: ") or "arn:aws:kms:us-east-1:900472373366:key/fcc2850b-c019-49bd-8a5c-22f823377776"
Customer1DataName = input("Please enter the Customer1DataName: ") or "customer1datatest"
cfnClient.create_stack(
    StackName = 'LunchCustomerEnvironment',
    TemplateURL = 'https://cf-templates-bmnpl599pfyc-us-east-1.s3.amazonaws.com/lunchVPC-VPN-S3.yml',
    Parameters = [
        {
            'ParameterKey' : 'S3Bucket1Name',
            'ParameterValue' : S3Bucket1Name
        },
        {
            'ParameterKey' : 'S3Bucket2Name',
            'ParameterValue' : S3Bucket2Name
        },
        {
            'ParameterKey' : 'Customer2AppServerInstanceType',
            'ParameterValue' : Customer2AppServerInstanceType
        },
        {
            'ParameterKey' : 'Customer2AppServerKeyName',
            'ParameterValue' : Customer2AppServerKeyName
        },
        {
            'ParameterKey' : 'Customer2AppServerImageId',
            'ParameterValue' : Customer2AppServerImageId
        },
        {
            'ParameterKey' : 'Customer2AppServerSubnetId',
            'ParameterValue' : Customer2AppServerSubnetId
        },
        {
            'ParameterKey' : 'Customer2AppServerSecurityGroup',
            'ParameterValue' : Customer2AppServerSecurityGroup
        },
        {
            'ParameterKey' : 'Customer1KMSKeyArn',
            'ParameterValue' : Customer1KMSKeyArn
        },
        {
            'ParameterKey' : 'Customer1DataName',
            'ParameterValue' : Customer1DataName
        },
        {
            'ParameterKey' : 'VpcCIDR',
            'ParameterValue' : VpcCIDR
        },
        {
            'ParameterKey' : 'VPCNAME',
            'ParameterValue' : VPCNAME
        },
        {
            'ParameterKey' : 'ClientSubCidr',
            'ParameterValue' : ClientSubCidr
        },
        {
            'ParameterKey' : 'AppSubCidr',
            'ParameterValue' : AppSubCidr
        },
        {
            'ParameterKey' : 'LambdaSubCidr',
            'ParameterValue' : LambdaSubCidr
        },
        {
            'ParameterKey' : 'EndpointCidrBlock',
            'ParameterValue' : EndpointCidrBlock
        },
        {
            'ParameterKey' : 'EndpointServerCert',
            'ParameterValue' : EndpointServerCert
        },
        {
            'ParameterKey' : 'ClientServerCert',
            'ParameterValue' : ClientServerCert  
        }
    ]
)