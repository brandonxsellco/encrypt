#!/bin/bash

## Get the logged in user's short name
userName=$( whoami )

## Get the logged in user's full name
fullName=$(dscl . read /Users/${userName} RealName | awk -F: '{print $NF}' | sed -e 's/^ *//;/^$/d')

## First check if the users file system is encrypted
printf "\nChecking if file system is encrypted ...\nPlease enter your password below \n\n"
fdeStatus="$(sudo fdesetup status)"

## Foward on data to Python processing server
printf "\nSending file system encryption status to processing server ..."

response=$(
    curl -H "Content-type: application/json" \
        -X POST \
        -d '{"userName":"'"$userName"'", "fullName":"'"$fullName"'", "fdeStatus":"'"$fdeStatus"'"}' \
        http://192.168.10.3:8080 \
        --write-out %{http_code} \
        --silent \
        --output /dev/null \
)

# If response code from server = 200, success
if [ $response = 200 ]; then
	printf "\nSuccessfully completed encryption check, thank you!\n"
  sleep 3
# Else error
else
  printf "\nEncryption check unsuccessful, please contact Brandon/Neil ...\n"
  sleep 3
fi
