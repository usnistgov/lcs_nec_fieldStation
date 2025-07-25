# changeDeployment.py

# Script used to switch which databases the station broadcasts to. Stations use different databases whether
#       they are in the lab or field
#
#       Original: T.P. Boyle 07/2025
import json
import os

def update_archive_field(file_path, use_lab):
    try:
        with open(file_path, 'r+') as file:
            data = json.load(file)
            if 'archive' in data:
                archive = data['archive']
                if archive['name'] in ['lcs_nec_stnArchiveMeasurements', 'lcs_nec_labArchiveMeasurements']:
                    data['archive'] = {
                        "name": "lcs_nec_labArchiveMeasurements" if use_lab else "lcs_nec_stnArchiveMeasurements",
                        "partition": "stn_id#s_name" if use_lab else "stn_loc#s_name",
                        "sortkey": "start_epoch"
                    }
                elif archive['name'] in ['lcs_nec_stnCalSequences', 'lcs_nec_labCalSequences']:
                    data['archive'] = {
                        "name": "lcs_nec_labCalSequences" if use_lab else "lcs_nec_stnCalSequences",
                        "partition": "stn_id#cal_type" if use_lab else "stn_loc#cal_type",
                        "sortkey": "cal_start_epoch"
                    }
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                print(f"Updated {file_path} for {'lab' if use_lab else 'field'} use")
            else:
                print(f"No 'archive' field found in {file_path}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON in {file_path}: {e}")

def update_stn_loc(use_lab):
    try:
        with open('/etc/environment', 'r') as file:
            lines = file.readlines()
    except PermissionError:
        print("Permission denied. Please run with sudo.")
        return

    new_lines = []
    stn_loc_updated = False
    for line in lines:
        if line.startswith('STN_LOC='):
            if use_lab:
                new_lines.append('STN_LOC="lab"\n')
            else:
                stn_loc = input("Enter the station location: ")
                new_lines.append(f'STN_LOC="{stn_loc}"\n')
            stn_loc_updated = True
        else:
            new_lines.append(line)

    if not stn_loc_updated:
        if use_lab:
            new_lines.append('STN_LOC="lab"\n')
        else:
            stn_loc = input("Enter the station location: ")
            new_lines.append(f'STN_LOC="{stn_loc}"\n')

    try:
        with open('/etc/environment', 'w') as file:
            file.writelines(new_lines)
        print("Updated STN_LOC in /etc/environment")
    except PermissionError:
        print("Permission denied. Please run with sudo.")

def main(directory, use_lab):
    for filename in os.listdir(directory):
        if filename.endswith('_metrics.json'):
            file_path = os.path.join(directory, filename)
            update_archive_field(file_path, use_lab)
    update_stn_loc(use_lab)

if __name__ == "__main__":
    directory = "/home/meso3/scripts/metrics_jsons"
    while True:
        config = input("Configure for lab or field use? (lab/field): ").lower()
        if config in ['lab', 'field']:
            use_lab = config == 'lab'
            break
        else:
            print("Invalid input. Please enter 'lab' or 'field'.")
    main(directory, use_lab)
    print("Please reboot system to apply new environment variable")
