1. Ssh into OpenVPN - Prod
2. sudo su
3. cd /usr/local/openvpn_as/scripts


### Show the current properties for all users:
./sacli UserPropGet

### Show the current properties for a specific user or group:
./sacli --pfilt "dmytro" UserPropGet

### Add a new user from scratch:
./sacli --user "dmytro" --key "type" --value "user_connect" UserPropPut

### Show the current properties for a specific user or group:
./sacli --pfilt "dmytro" UserPropGet

### Add a user to a group:
./sacli --user "dmytro" --key "conn_group" --value "Admin" UserPropPut


### Password
./sacli --user dmytro --new_pass Y+0/xoC4Y3B5 setLocalPassword


### Google Auth
./sacli --user dymtro GoogleAuthRegen

### Add User to Group
./sacli --user "dmytro" --key "conn_group" --value "Admin" UserPropPut

./sacli --user dmytro --key "pvt_google_auth_secret" --value "O34V3SIXBKUWFDXE" UserPropPut

./sacli --user dmytro --key "pvt_google_auth_secret_locked" --value "true" UserPropPut

Enable TOTP MFA for a specific user or group:
./sacli --user dmytro --key "prop_google_auth" --value "true" UserPropPut
./sacli start