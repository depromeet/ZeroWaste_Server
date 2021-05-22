import boto3
import os
import json
from rest_framework.request import Request
from zerowaste.zerowaste.settings import AWS_STORAGE_BUCKET_NAME

# upload_file_test
# conn = boto3.connect_s3()
# url = conn.generate_url(120, 'POST', bucket=AWS_STORAGE_BUCKET_NAME, key=text.txt)

# give multiple singed-urls to response
def get_singed_url(n):
    singed_urls = []
    s3_bucket = os.environ.get(AWS_STORAGE_BUCKET_NAME)
    file_name = Request.args.get('file_name')
    file_type = Request.args.get('file_type') # request에서 type 지정 가능한가?

    s3 = boto3.client('s3')

    for i in range(n):
        presigned_post = s3.generate_presigned_post(
            Bucket = s3_bucket,
            Key = file_name,
            Fields = {"acl": "public-read", "Content-Type": file_type},
            Conditions = [
                {"acl" : "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )
    singed_urls.append(json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (s3_bucket, file_name)
    }))
    return singed_urls