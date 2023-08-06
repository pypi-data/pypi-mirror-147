import boto3
from datetime import datetime,date
from datetime import datetime, timedelta
import os
import os.path
import sys   
import fnmatch

def download_s3_file(bucket_name, s3_folder,file_extension, destination_path=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        destination_path: a relative or absolute directory path in the local file system
        file_extension: extension of file such as .parquet or .csv 
    """
    s3 = boto3.resource('s3') 
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        if obj.key.endswith(f"{file_extension}"):
            target = obj.key if destination_path is None \
                else os.path.join(destination_path, os.path.relpath(obj.key, s3_folder))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            print(target)
            bucket.download_file(obj.key, target)
        else:
            print("No file found! check s3_folder and file_extension")

def upload_s3_file(bucket_name,source_path,base_dir,file_extension):
    """
    upload the contents of a folder directory to the s3 path
    Args:
        bucket_name: the name of the s3 bucket
        source_path: local dirctory where file is located
        base_dir: a relative or absolute directory path in the local file system
        file_extension: extension of file such as .parquet or .csv 
    """
    print(f'Base Dir:{base_dir}')
    print(f'Source Dir:{source_path}')
    s3 = boto3.resource('s3') 
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(f"{file_extension}"):
                local_dir=(os.path.join(root, file))
                s3_path_dir=f'{local_dir.split(base_dir)[1] }'
                print(s3_path_dir)
                s3.Bucket(bucket_name).upload_file(local_dir, s3_path_dir)
            else:
                print("No file found! check source_path and file_extension")