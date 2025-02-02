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

    # obtenir la liste des fichiers qui existe dans le bucket_name
    response = s3.list_objects_v2(Bucket=bucket_name)
    bucket_files = {obj['Key']: obj for obj in response.get('Contents', [])}

    # la liste des fichiers locaux (sur le dossier folder_path)
        # le path est aussi sauvgarder \folder_path\filename pour verifier avec les fichier sur les buckets
        # en respectent la notion des clés qui representent l'arboresence 
    onlyfiles = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            onlyfiles.append(full_path)
    
    # 1er et 3eme cas dans la meme boucle (verfier si le fichier local existe sur le bucket et si il est a jour)
    for local_file in onlyfiles:
        #car le premier / est retirer car les clés des bucket ne contenant pas un / en premier (sinon il n'arrivera pas a comparer entre les 2 --> n'existe pas toujours)
        if local_file.lstrip('/') not in bucket_files:
            print(f"cas 1 : local file: {local_file} n'existe pas dans le bucket {bucket_name} --> uploading")
            s3.upload_file(local_file, bucket_name, local_file)
        else:
            # cas 3 : vérifier si la version locale est plus récente que celle dans le bucket
            local_modified_time = os.path.getmtime(local_file)
            bucket_modified_time = bucket_files[local_file.lstrip('/')]['LastModified'].timestamp()
            if local_modified_time > bucket_modified_time:
                print(f"cas 3 : Local file {local_file} est plus recent que celui dans le bucket {bucket_name} --> updating")
                s3.upload_file(local_file, bucket_name, local_file)
 
    #2eme cas : supprimer les fichier qui sont dans le bucket mais qui ne sont pas dans le local 
    local_files = set(f.lstrip('/') for f in onlyfiles) #retirer le / dans les debut des noms des fichiers pour comparer 
    for bucket_file in bucket_files:
        if bucket_file not in local_files and bucket_file.startswith(folder_path.lstrip('/')):
            print(f"cas 2 : le fichier {bucket_file} n'existe pas en local --> deleting")
            s3.delete_object(Bucket=bucket_name, Key=bucket_file)



if __name__ == "__main__":

    folder_path = sys.argv[1]
    bucket_name = sys.argv[2]
    s3 = init_s3_minio('http://172.17.0.2:9000', 'minio', 'miniokey')
    synchronisationS3(s3,folder_path,bucket_name)
    print('------- fin de programme -----------')
