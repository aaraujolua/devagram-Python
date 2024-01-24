import boto3
from decouple import config
from botocore.exceptions import ClientError

class AWSProvider:
    def upload_file_s3(self, path_to_save, file_path, bucket='devagram-python-lua'):
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id =config('AWS_ACCESS_KEY'),
            aws_secret_access_key = config('AWS_SECRET_KEY')
        )
        
        try:
            s3_client.upload_file(file_path, bucket, Key=path_to_save)
            
            url = s3_client.generate_presigned_url('get_object', ExpiresIn=0, Params={'Bucket': bucket, 'Key': path_to_save})
            
            return str(url).split("?")[0]
            
        except ClientError as error:
            return False