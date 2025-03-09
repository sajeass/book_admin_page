# -*-coding: utf-8 -*-
import os
import mimetypes
from azure.storage.blob import BlobServiceClient, ContentSettings
import src.common.helper as helper

class File_control(object):

    def __init__(self, file_name, container_name, contents=None, blob_path=None, root_folder=None, test_mode='off', metadata={}):
        # Determine the root folder based on the environment
        # File_control 클래스에서 root_folder 설정 수정
        if root_folder is None:
            if os.getenv('AWS_EXECUTION_ENV'):
                # For AWS Lambda environment
                root_folder = '/tmp/temp_files/'
            elif helper.is_ubuntu():
                # For web servers (Ubuntu environment)
                root_folder = '/var/www/crawler_webserver/temp_files/'
            else:
                # For local development
                root_folder = os.path.join(os.getcwd(), 'temp_files')

        os.makedirs(root_folder, exist_ok=True)  # Ensure the folder exists

        self.file_name = file_name
        self.file_path = os.path.join(root_folder, self.file_name)
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv('AZURE_STORAGE_CONNECTION_STRING',
                      "DefaultEndpointsProtocol=https;AccountName=aboutbstorage;AccountKey=UaUj+hK/Q8HfZgiucYa64sKF146R8ToVYdDzxFgjXQbkW1s/nn+swWrQXK4EFUbYza3dMUHbw4V+Bm+rV9piJQ==")
        )
        if test_mode == 'on':
            self.container_name = 'test'
        self.contents = contents
        self.blob_path = blob_path if blob_path is not None else file_name
        self.content_type = mimetypes.guess_type(self.file_name)[0]
        self.metadata = metadata

    def download(self):
        """Download content and save it to a file."""
        with open(self.file_path, 'wb') as f:
            f.write(self.contents)

    def upload(self):
        """Upload a file to Azure Blob Storage and delete the local file after upload."""
        self.download()
        if os.path.isfile(self.file_path):
            container_client = self.blob_service_client.get_container_client(self.container_name)
            try:
                with open(self.file_path, 'rb') as data:
                    container_client.upload_blob(
                        name=self.blob_path,
                        data=data,
                        content_settings=ContentSettings(content_type=self.content_type),
                        metadata=self.metadata,
                        overwrite=True  # Allow overwriting the existing blob
                    )
                # 파일 업로드 성공 후 삭제
                blob_url = f"{self.blob_service_client.primary_endpoint.strip('/')}/{self.container_name}/{self.blob_path.lstrip('/')}"
                print(f"File URL: {blob_url}")
                os.remove(self.file_path)
            except Exception as e:
                print(f"Failed to upload file: {self.file_path}. Reason: {e}")

    def delete(self):
        """Delete a local file."""
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    def check_file_exists(self):
        """Check if a file exists in Azure Blob Storage."""
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=self.blob_path)
        return blob_client.exists()