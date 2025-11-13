import boto3
import os.path
from io import BytesIO


class S3:
    def uploadfile(self, path, files, file_names, aws_key_id, aws_secret, aws_bucket):
        session = boto3.session.Session()


        s3 = session.client(service_name='s3',
                            region_name='ru-central1',
                            endpoint_url='https://storage.yandexcloud.net',
                            aws_access_key_id=aws_key_id,
                            aws_secret_access_key=aws_secret)

        for i, file in enumerate(files):
            file.file.seek(0)
            filename = os.path.join(path, file_names[i]).replace("\\", "/")
            s3.upload_fileobj(file.file, aws_bucket, filename)

        return

    def downloadfile(self, filename, aws_key_id, aws_secret, aws_bucket):
        output = BytesIO()

        session = boto3.session.Session()

        s3 = session.client(service_name='s3',
                            region_name='ru-central1',
                            endpoint_url='https://storage.yandexcloud.net',
                            aws_access_key_id=aws_key_id,
                            aws_secret_access_key=aws_secret)

        s3.download_fileobj(Bucket=aws_bucket, Key=filename, Fileobj=output)

        return output.getvalue()

    def deletefile(self, filename, aws_key_id, aws_secret, aws_bucket):
        session = boto3.session.Session()


        s3 = session.client(service_name='s3',
                            region_name='ru-central1',
                            endpoint_url='https://storage.yandexcloud.net',
                            aws_access_key_id=aws_key_id,
                            aws_secret_access_key=aws_secret)

        deleted = s3.delete_object(Bucket=aws_bucket, Key=filename)

        return deleted

    def uploaded_list(self, path, aws_key_id, aws_secret, aws_bucket):
        session = boto3.session.Session()

        s3 = session.client(service_name='s3',
                            region_name='ru-central1',
                            endpoint_url='https://storage.yandexcloud.net',
                            aws_access_key_id=aws_key_id,
                            aws_secret_access_key=aws_secret)

        list = []
        if path:
            for key in s3.list_objects(Bucket=aws_bucket, Prefix=path)['Contents']:
                list.append(key['Key'])
        else:
            for key in s3.list_objects(Bucket=aws_bucket)['Contents']:
                list.append(key['Key'])

        return list