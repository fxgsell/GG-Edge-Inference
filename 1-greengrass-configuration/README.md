# Introduction

This lab will guide the user through 
- TODO

## Setup AWS resources

1. Create a new S3 bucket in region `us-east-1` for this workshop, this bucket will be used to host your ML models
1. Create a new AWS Lambda, this function will be used for inference:
    - Choose `ml-edge-workshop-lab-1` as the function name
    - Choose `Python 2.7` as the runtime,
    - Create an alias `latest` pointing to `$LATEST`

## Creating

1. Setup Cloud9 environment

1. From your desktop/laptop, run `python3 create-greengrass-config.py --create-group GG-ML-Workshop --bucket my-greengrass-models --function ml-edge-workshop-lab-1`
    - Set the 3 parameters: a new **Group Name** and the same values that you choose in the previous steps for the **bucket** and the **function** names.

1. Configure your device with the `certificates.tar.gz` file.
    - Triple-pres the button S3 or REC.
    - If you know the IP of the device connect to it on port 80.
    - Upload `certificates.tar.gz` and don't forget to click **Finished**.

1. Go to the AWS console and hit Deploy in your Greengrass Group (Choose "Automatic Detection" at the first step).

1. Once the deployment finished you can go look in the console or run `python3 create-greengrass-config.py --ip-address` to get  all the IPs of your device.

You're now set to start doing some ML @Edge.

## Usage

### Create Group

`python3 create-greengrass-config.py --create-group <GROUP_NAME> --bucket <BUCKET_NAME> --function <FUNCTION_NAME>`

### Delete Group

`python3 create-greengrass-config.py --delete-group`

### Get IP Address

`python3 create-greengrass-config.py --ip-address`
