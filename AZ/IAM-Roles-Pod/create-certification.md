1. Creat certificate for CA
openssl genrsa -out ca.key 2048

2. Create CSR for CA
openssl req -new -key ca.key -subj"/CN=KUBERNETES-CA" -out ca.csr

3. Signed the serticicate usinf x509 command
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt



4. Creat certificate for admin
openssl genrsa -out admin.key 2048

2. Create CSR for admin
openssl req -new -key admin.key -subj"/CN=kube-admin,/O=system:masters" -out admin.csr

3. Signed the serticicate using x509 command
openssl x509 -req -in admin.csr -CA ca.key -CAkey ca.key -out admin.crt


HOw to use this key to authentication\

curl https://kube-apiserver:6443/api/v1/pods --key admin.key --cert admin.crt --cacert ca.crt
or
Use this details in kube-config file
