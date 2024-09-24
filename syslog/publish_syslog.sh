  GNU nano 5.4                                                                                                                         publish_syslog.sh
# #!/usr/bin/env bash

# Script used to tail jornalctl, convert entries to mqtt json packets
#
#       Original: T.P. Boyle 08/2024
#       Modified: T.P. Boyle 09/2024 - added pkt_type parameter for AWS validation

trap "echo 'Terminating...'; exit" SIGINT SIGTERM

source /etc/environment
topic="sl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/syslog"

while true; do

  journalctl -f | while read line; do

    escaped_line=${line//[\/\"]/ }

    # Extract the timestamp and convert it to ISO 8601 format
    epoch_timestamp=$(date +%s)

    # Get device type and OS version from environment variables
    device_type=$(uname -m)
    os_version=$(lsb_release -ds)

    # Create a JSON document with additional fields
    json_data="{
        \"timestamp\": $epoch_timestamp,
        \"pkt_type\": \"syslog\",
        \"stn_id\": \"$STN_NAME\",
        \"stn_loc\": \"$STN_LOC\",
        \"topic\": \"$topic\",
        \"syslog\": {
                \"loggroup\": \"station_logs\",
                \"logstream\": \"$STN_NAME\"
        },
        \"message\": {
                \"hostname\": \"$HOSTNAME\",
                \"device_type\": \"$device_type\",
                \"os_version\": \"$os_version\",
                \"body\": \"$escaped_line\"
        }
    }"

    # Write the JSON document to a file
    echo "$json_data" > /home/meso3/syslog/journal_entry.json
    mosquitto_pub  -q 1 -t $topic -f /home/meso3/syslog/journal_entry.json

  done

done
