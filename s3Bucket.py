import boto3


def createbucket(bucket_name, bucket_location='None'):
    if bucket_location is None:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client = boto3.client('s3', region_name=bucket_location)
        location = {'LocationConstraint': bucket_location}
        s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
    return "created"



def listallbuckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    bucketlist=[]
    print('The Existing Buckets on the AWS account are: ')
    for buck in response['Buckets']: 
        bucketlist.append(f' {buck["Name"]}')
    return bucketlist


def uploadfile(file_name, bucket_name):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket_name, object_name)
    return "uploaded"