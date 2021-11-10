import config
import boto3

client = boto3.client('s3')

resource = boto3.resource('s3')
my_bucket = resource.Bucket(config.aws_bucket)

json_files = list(my_bucket.objects.filter(Prefix=config.aws_folderPrefix))

data = []

obj = json_files[0].get()

print(obj)
