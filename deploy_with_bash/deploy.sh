#!/bin/bash

servers=("<@server1>" "<@server2>" "<@servern>")
package_path="syncs3_package.deb"
remote_path="/tmp/syncs3_package.deb"
user_name="admin"

# deploy the package on each server in the servers list
for server in "${servers[@]}"
do
  # copy the .deb file to the remote server
  scp $package_path $user_name@$server:$remote_path

  # install python3 and boto3 if necessary
  ssh $user_name@$server "which python3 >/dev/null 2>&1 || sudo apt-get install -y python3"
  ssh $user_name@$server "python3 -m pip --version >/dev/null 2>&1 || sudo apt-get install -y python3-pip"
  ssh $user_name@$server "python3 -m pip show boto3 >/dev/null 2>&1 || python3 -m pip install boto3"

  # install the .deb package on the remote server
  ssh $user_name@$server "sudo dpkg -i $remote_path && rm $remote_path"

  echo "deployment of syncs3_package.deb completed on server $server"
done
