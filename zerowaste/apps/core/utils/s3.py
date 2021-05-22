import boto3
from datetime import datetime
from django.conf import settings
from botocore.client import Config


def sign_upload(counts, user_id):
    s3 = boto3.client('s3', config=Config(signature_version=settings.AWS_SIGNATURE_VERSION, region_name=settings.AWS_REGION))
    result = []
    for i in range(counts):
        key = 'users/' + str(user_id) + '/' + str(int(datetime.now().timestamp()))
        signed_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
            ExpiresIn=3600,
            HttpMethod='PUT',
        )
        result.append({
            'signed_url': signed_url,
            'public_url': 'https://%s.s3.amazonaws.com/%s' % (settings.AWS_STORAGE_BUCKET_NAME, key)
        })
    return result
