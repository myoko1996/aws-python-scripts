import boto3
import schedule
import time

def create_volume_snapshots(region_name):
    try:
        ec2_client = boto3.client('ec2', region_name=region_name)
        volumes = ec2_client.describe_volumes(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['prod']
                }
            ]
        )
        for volume in volumes['Volumes']:
            new_snapshot = ec2_client.create_snapshot(
                VolumeId=volume['VolumeId']
            )
            print(f"Snapshot created in {region_name}:", new_snapshot)
    except Exception as e:
        print(f"An error occurred in {region_name}:", e)

# List of regions where you want to create snapshots
regions = ["eu-west-3", "us-west-2", "ap-southeast-1"]

# Schedule snapshot creation for each region every day
for region in regions:
    schedule.every().day.do(create_volume_snapshots, region_name=region)

while True:
    try:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 1 minute before checking again
    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
    except Exception as e:
        print("An error occurred during scheduling:", e)
