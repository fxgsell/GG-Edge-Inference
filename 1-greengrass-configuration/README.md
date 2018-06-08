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

Amazon Cloud9 is a web-based IDE -- we will use it to configure the Greengrass settings for the target device.

1. From the AWS console, go to the [Amazon Cloud9](https://console.aws.amazon.com/cloud9/home?region=us-east-1) console and select the **Create Environment** button to fill in the following information:
    1. Step 1: Name environment
        - *Environment name*: `ml-edge-workshop-lab-1` 
        - *Description*: <blank>
        - Click **Next Step** to proceed
    1. Step 2: Configure settings
        - Leave the defaults, and click **Next Step** to proceed
    1. Step 3: Review
        - Click **Create Environment** to finish and begin IDE environment creation
   If successfully, you should now be in your new Cloud9 environment. We will now clone this git repository so we have access to this and other labs throughout the remainder of the workshop.

1. From the Getting Started panel on the right of the IDE, select **Clone Git Repository** and provide the URL of this repository (ie. https://github.com/zukoo/GG-Edge-Inference):
```
git clone https://github.com/zukoo/GG-Edge-Inference
```

1. We will now switch to the directory for Lab 1 content and perform some necessary setup of our environment before we begin:
```
cd GG-Edge-Inference/
cd 1-greengrass-configuration/
export PATH=/opt/c9/python3/bin:$PATH
pip3 install boto3
```

1. Within this directory, we will use the `create-greengrass-config.py` script to generate the necessary groups for publishing our Greengrass function:

```
python3 create-greengrass-config.py --create-group ml-edge-workshop --bucket ml-edge-workshop-lab-1 --function ml-edge-workshop-lab-1
```
    
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
