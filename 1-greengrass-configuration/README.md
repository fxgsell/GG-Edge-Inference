# Get started

1. Create an S3 bucket to host the models.

1. Create the lambda for inference:
    - Choose the `Python 2.7` runtime,
    - Create an alias `latest` pointing to `$LATEST`,

1. Run `python3 create-greengrass-config.py --create-group GG-ML-Workshop --bucket my-greengrass-models --function demo-inference`
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