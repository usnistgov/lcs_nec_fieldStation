
# This script flattens json output from redis_to_json, used by json_to_log.sh
#
# 	Original: T.P. Boyle 08/2025
#	Modified: T.P. Boyle 08/2024 -  Modified to add metrics packet via jq, send to local MQTT bridge

import json
import csv
import sys

def flatten_json(data, prefix=''):
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result.update(flatten_json(value, prefix + key + '_'))
        else:
            result[prefix + key] = value
    return result

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        data = json.load(f)

    flattened_data = flatten_json(data)

    fieldnames = list(flattened_data.keys())

    with open(output_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(flattened_data)

if __name__ == '__main__':
    main()
