import boto3
import os

def upload_files(path):
    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name='ap-northeast-2'
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('omega-django-onlineshop')

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key="media/"+(full_path.replace("\\","/"))[len(path) + 1:], Body=data, ACL='public-read')


if __name__ == "__main__":
    upload_files('./media')