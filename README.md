# S3 Bucket Synchronization Project

## Introduction
This project consists of a script to synchronize a local directory with an S3 bucket. It can upload local files that are not present in the bucket, update more recent local files, and delete files in the bucket that no longer exist locally.


## Prerequisites
* **Python 3**

* **boto3:** The Python library for interacting with S3

* **Debian/Ubuntu:** The script is packaged as a .deb file for easy installation on Debian-based systems.


## Installation
### Pre-Installation

Navigate to the directory **s3_synch/syncs3_package/usr/local/bin** and verify that the line matches your S3 service address and credentials.

```
s3 = init_s3_minio('http://172.17.0.2:9000', '<Access Key>', '<Secret Key>')
```
* **Service Address:** Replace `http://172.17.0.2:9000` with the endpoint URL of your S3-compatible service.

* **Access Key:** Replace **\<Access Key>** with your actual S3 access key.

* **Secret Key:** Replace **\<Secret Key>** with your S3 secret key.

### Installation via the **.deb** Package

1. **Build the package:** Use the following command to build the package:
```
dpkg-deb --build syncs3_package
```

2. **Install the package:** Install the package with the following command:
```
sudo dpkg -i syncs3_package.deb
```

## Usage 
To synchronize a local directory with an S3 bucket, use the following command:
```
synchronisation-s3 <local_directory_path> <bucket_name>
``` 
* **\<local_directory_path>:** The path to the local directory you want to synchronize.

* **\<bucket_name>:** The name of the S3 bucket to synchronize with.

### Example 
```
synchronisation-s3 /home/user/data test-bucket
```


## Deployement on multipe servers
### 1. Using Ansible 
Before running the Ansible playbook, edit the server addresses in the `deploy_with_ansible\inventory.yml` file to reflect the IP addresses or hostnames of your target servers and the **ansible_user**.

Once the addresses are updated, run the playbook with the following command:
```
ansible-playbook -i inventory.yml deploy_s3_sync_deb.yml
```

### 2. Using a Bash Script 
Before running the Bash script, edit the server addresses in the following variable of `deploy_with_bash/deploy.sh`:
```
servers=("<@server1>" "<@server2>" "<@servern>")
```
The Bash script **deploy.sh** allows deploying the package to multiple servers using SSH and SCP. To use it, run the following command:
```
./deploy.sh
```

## Contact 
For any questions or assistance, you can contact me at: ramdani.abderrahmane213@gmail.com

