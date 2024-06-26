# Test file transfer rate form local machine to s3 in 2 different no_proxy condition, one with amazonaws.com
### To get access key and secret key
```sh
kubectl --kubeconfig -n brown-dev-001 get secret
kubectl --kubeconfig dev -n brown-dev-001 get secret mlpipeline-minio-artifact -o yaml
kubectl -n brown-dev-001 get secret mlpipeline-minio-artifact -o yaml
```

### From secret get encoded accesskey and secretkey file
```t
accesskey: QUtJXXXXXXXXXXXXzTVpFUFk=
secretkey: THAwXXXXXXXXXX4OQ==
```

### Decode access key and secret key
```sh
echo QUtJQVXXXXXXXXXXXXXXXXXXXXpFUFk= | base64 --decode
echo THAwRXXXXXXXXXXXXXXXXXXXxQVdzOFNSU1Y4OQ== | base64 --decode
```

### Now you have decoded access and secret file
```t
AKXXXXXXXXXX3MZEPY
Lp0XXXXXXXXXXXXXXXXXXXXXXWs8SRSV89
eu-west-1
```

### Create awscli dev profile using above cred
```
aws configure --profile dev
```
### get proxy in one server with amazon
```sh
echo $no_proxy
export no_proxy=10.0.0.0/8,172.29.0.0/8,astrazeneca.net,localhost,127.0.0.1,::1
```

### get proxy in another server with amazon
```sh
export no_proxy=$no_proxy,amazonaws.com,.kubeflow
echo $no_proxy
```
### Download test file
```
curl -LO https://testfile.org/file-1GB
mv file-1GB test-file.zip
```

### set var for brnach name and file name
```sh
BUCKET=az-eu-azimuth-kfp-dev/artifacts/brown-dev-001
FILE=test-file.zip

echo $BUCKET
echo $FILE
```

### Create test script 
- name: **s3-cp-speed-test.sh**
```sh
#! /bin/bash
#Author : Kiran Murugulla
#Description : Script to create an asset and upload binary from local machine into an S3 bucket

usage="Usage: s3-cp-speed-test.sh bucketname filepath \n"
BUCKET=$1
FILE=$2
if [ ! $# -eq 2 ] ; then
echo -e "$usage"
exit 2


fi

echo -e "Starting Copy $FILE into s3 bucket $BUCKET"
FILESIZE=$(stat -c%s "$FILE")
#echo "Size of $FILENAME = $FILESIZE bytes."
START_TIME=$SECONDS
aws s3 cp $FILE s3://$BUCKET --profile dev
ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo -e "Completed uploading binaries ."
echo -e " File $FILE of size $FILESIZE bytes copied to s3 Bucket $BUCKET in : $(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec \n"
echo ""
#Verify the file uploaded
echo -e "Verifying the File Copied over correctlly - S3 Listing "
echo ""
aws s3 ls s3://$BUCKET/$FILE --profile dev
echo ""
echo "Delete the file"
echo ""
aws s3 rm s3://$BUCKET/$FILE --profile dev
echo ""
```

### Give execution permission
```sh
chmod +x s3-cp-speed-test.sh
```

### test script
```sh
./s3-cp-speed-test.sh $BUCKET $FILE
```

### Test Condition:
```t
Used 500 Mb file
from 2 different server


Result
Serve 1
echo $no_proxy: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net,localhost,127.0.0.1,::1
File test-file.zip of size 524288000 bytes copied to s3 Bucket az-eu-azimuth-kfp-dev/artifacts/brown-dev-001 in : 1 min 2 sec 

server 2
10.0.0.0/8,172.29.0.0/8,astrazeneca.net,localhost,127.0.0.1,::1,amazonaws.com
File test-file.zip of size 524288000 bytes copied to s3 Bucket az-eu-azimuth-kfp-dev/artifacts/brown-dev-001 in : 0 min 23 sec 
```

edit no_proxy value in azimuth-images/.github/workflows/main.workflow.yaml
```
env:
  ## Sets environment variable for internet access
  http_proxy: http://azpzen.astrazeneca.net:9480
  https_proxy: http://azpzen.astrazeneca.net:9480
  no_proxy: 10.0.0.0/8,172.29.0.0/8,astrazeneca.net
```
Change no_proxy value in azimuth-images Azimuth 
merge PR
Rebuild in demo
restart workbeanch
test transfer rate gain
Create Blog
