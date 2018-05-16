# Get started

1. Create an S3 bucket to host the models.

1. Create the lambda for inference:
    - Choose the `Python 2.7` runtime,
    - Create an alias `latest` pointing to `$LATEST`,

1. Run `python3 create-greengrass-config.py --create-group GG-ML-Workshop --bucket my-greengrass-models --function demo-inference`
    - Set the 3 parameters's values: a new **Group Name** and the same values that you choose in the previous steps for the **bucket** and  the **function** names.

1. Upload the resulting `certificates.tar.gz` on your device.

1. Go back to the console and hit Deploy in your Greengrass Group. (Choose "Automatic Detection" at the first step)

1. Once the deployment finished you can go look in the console or run `python3 create-greengrass-config.py --ip-address` to get the IP of your device.

You're now set to start doing some ML @Edge.

## Usage

### Create Group

`python3 create-greengrass-config.py --create-group <GROUP_NAME> --bucket <BUCKET_NAME> --function <FUNCTION_NAME>`

### Delete Group

`python3 create-greengrass-config.py --delete-group`

### Get IP Address

`python3 create-greengrass-config.py --ip-address`