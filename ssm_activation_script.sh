# Script used to attach device to SSM. BE SURE TO UPDATE "" PARAMETERS!

#mkdir ~/ssm
cd ~/ssm
curl https://amazon-ssm-us-east-1.s3.us-east-1.amazonaws.com/latest/debian_arm/ssm-setup-cli -o ./ssm-setup-cli
chmod +x ./ssm-setup-cli
apt update
apt install gcc-10-base:armhf krb5-locales libc6:armhf libcom-err2:armhf libcrypt1:armhf libgcc-s1:armhf libgssapi-krb5-2:armhf libidn2-0:armhf libk5crypto3:armhf libkeyutils1:armhf libkrb5-3:armhf libkrb5support0:armhf libnsl2:armhf libnss-nis:armhf libnss-nisplus:armhf libssl1.1:armhf libtirpc3:armhf libunistring2:armhf
./ssm-setup-cli -register -activation-code "your_activation_code" -activation-id "your_activation_id" -region "us-east-1"
