import os
import sys
import boto3

def init_s3_minio(endpoint_url, access_key_minio, secret_key_minio):
    s3_client=boto3.client('s3',
                            endpoint_url=endpoint_url,
                            aws_access_key_id=access_key_minio,
                            aws_secret_access_key=secret_key_minio
                    )
    return s3_client

def synchronisationS3(s3,folder_path,bucket_name):

    # Get the list of files in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    bucket_files = {obj['Key']: obj for obj in response.get('Contents', [])}

    # Get the list of local files in the specified directory
    # The path is stored as full_path to compare with bucket keys
    # while respecting the key structure that simulates a directory hierarchy. 
    onlyfiles = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            onlyfiles.append(full_path)
    # Check if the local file exists in the bucket and if it's up to date
    for local_file in onlyfiles:
        # Remove leading slashes from the local file path for comparison
        if local_file.lstrip('/') not in bucket_files:
            print(f"local file {local_file} does not exist in bucket {bucket_name} --> uploading")
            s3.upload_file(local_file, bucket_name, local_file)
        else:
            # Check if the local file is more recent than the one in the bucket
            local_modified_time = os.path.getmtime(local_file)
            bucket_modified_time = bucket_files[local_file.lstrip('/')]['LastModified'].timestamp()
            if local_modified_time > bucket_modified_time:
                print(f"local file {local_file} is more recent than the file in bucket {bucket_name} --> updating")
                s3.upload_file(local_file, bucket_name, local_file)
 
    # Delete files in the bucket that no longer exist locally 
    local_files = set(f.lstrip('/') for f in onlyfiles) # Remove leading slashes for comparison
    for bucket_file in bucket_files:
        if bucket_file not in local_files and bucket_file.startswith(folder_path.lstrip('/')):
            print(f"the file {bucket_file} does not exist locally --> deleting")
            s3.delete_object(Bucket=bucket_name, Key=bucket_file)



if __name__ == "__main__":

    folder_path = sys.argv[1]
    bucket_name = sys.argv[2]
    s3 = init_s3_minio('http://172.17.0.2:9000', 'minio', 'miniokey')
    synchronisationS3(s3,folder_path,bucket_name)
    print('------- End of program -----------')
