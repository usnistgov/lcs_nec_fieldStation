# #!/usr/bin/env bash

# Script used to tail jornalctl, convert entries to mqtt json packets 
#
#	Original: T.P. Boyle 08/2024

source /etc/environment
topic="st/raw/$STN_OWNER/$STN_LOC/$STN_NAME/syslog"


journalctl -f | while read line; do
    # Extract the timestamp and convert it to ISO 8601 format
    epoch_timestamp=$(date +%s)

    # fix issues caused by qoutes in the log response
    esc_line=${line//[\/\"]/ }

    # Get device type and OS version from environment variables
    device_type=$(uname -m)
    os_version=$(lsb_release -ds)

    # Create a JSON document with additional fields
    json_data="{
        \"timestamp\": $epoch_timestamp,
        \"stn_id\": \"$STN_NAME\",
        \"stn_loc\": \"$STN_LOC\",
        \"topic\": \"$topic\",
	\"message\": {
		\"hostname\": \"$HOSTNAME\",
		\"device_type\": \"$device_type\",
		\"os_version\": \"$os_version\",
		\"body\": \"$esc_line\"
	}
    }"

    # Write the JSON document to a file
    echo "$json_data" > journal_entry.json
    cat journal_entry.json
    mosquitto_pub  -q 1 -t $topic -f journal_entry.json
done

