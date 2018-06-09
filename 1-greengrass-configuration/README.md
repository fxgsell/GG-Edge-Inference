# Introduction

This lab will guide the user through 
- TODO

## Setup AWS resources

1. Create a new S3 bucket in region `us-east-1` for this workshop, this bucket will be used to host your ML models
1. Create a new AWS Lambda, this function will be used for inference:
    - Choose `ml-edge-workshop-lab-1` as the function name
    - Choose `Python 2.7` as the runtime,
    - Create an alias `latest` pointing to `$LATEST`

## Creating your Cloud9 Environment (optional)

Amazon Cloud9 is a web-based IDE -- we will use it to configure the Greengrass settings for the target device and execute different AWS commands. 

> **Alternatively, you can simply clone this repository and run from your own computer (assuming that you have Python3 and boto3 correctly installed and user permissions are sufficient to execute on your AWS account). If so, please go directly to [Clone Workshop Content - Local](#clone-workshop-content---local)**

1. From the AWS console, go to the [Amazon Cloud9](https://console.aws.amazon.com/cloud9/home?region=us-east-1) console and select the **Create Environment** button to fill in the following information:
    1. Step 1: Name environment
        - *Environment name*: `ml-edge-workshop-lab-1` 
        - *Description*: *\<blank/empty\>*
        - Click **Next Step** to proceed
    1. Step 2: Configure settings
        - Leave the defaults, and click **Next Step** to proceed
    1. Step 3: Review
        - Click **Create Environment** to finish and begin IDE environment creation
   If successfully, you should now be in your new Cloud9 environment. We will now clone this git repository so we have access to this and other labs throughout the remainder of the workshop.
1. Once successfully launched, you will then see the following Welcome screen as shown here:
![Cloud9 Welcome](./images/cloud9_welcome.png)
1. Click the gear icon in the upper right of the environment, which will open a new tab in Cloud9 for setting Preferences (your screen colors may vary):
![Cloud9 Environment Settings](./images/cloud9_settings.png)
1. Select the AWS Settings tab on the left, and then disable the **AWS managed temporary credentials** option (which is on by default) ![Cloud9 AWS Settings](./images/cloud9_disable_aws_credentials.png)
1. Close the Preferences tab at the top, returning to the Welcome tab.

## Setting AWS IAM role - Cloud9

Your Cloud9 development environment is a running EC2 instance in your region and default VPC. We will now make a change to that instance so that we will have the superpowers necessary to perform administrative tasks in your AWS environment.

> **Caution: we will be applying additional policy for the Cloud9 environment to act on your behalf by attaching an IAM role to the underlying EC2 instance. Best practice would be to create a bespoke IAM policy to limit the potential actions performed from Cloud9, which is why we are making this additional change to elevate privileges. To ensure the safety of your environment, you should close and terminate this Cloud9 instance after completion of this workshop.**

1. Go to your AWS console, in the specific region where you launched your Cloud9 instance, and select to view your EC2 instances.
1. Identify the instance that is connected to your Cloud9 instance, which will be named as **aws-cloud9-...** where **...* will be both the name you assigned to your instance and a unique identifier
1. Select this instance, and under the **Actions** button, select the **Instance Settings** > **Attach/Replace IAM Role**.
![Cloud9 EC2 Instance - Replace IAM Role](./images/ec2_replace_iam_role.png)
1. Next, click the **Create new IAM role** link.
1. Next, click **Create Role** button.
1. Next, from the Create Role screen, select **AWS Service** from the top, followed by **EC2** then click the **Next: Permissions** button:
![Cloud9 EC2 Instance - Create IAM Role](./images/iam_create_role_1.png)
1. Next, attach the AdministratorAccess policy to this role and click the **Next: Review** button
![Cloud9 EC2 Instance - Create IAM Role](./images/iam_create_role_2.png)
1. Next, enter a role name for this role that will help identify it for use and later deletion (`ml-edge-workshop-cloud9-ec2` in our example), and click **Create Role** button. 
![Cloud9 EC2 Instance - Create IAM Role](./images/iam_create_role_3.png)
1. Now that we have created a role for our Cloud9 EC2 instance, we will assign it within the earlier screen. You should be able to click the Refresh (circular arrow) button and then filter for the new role you created, then click **Apply** button:
![Cloud9 EC2 Instance - Assign Role](./images/ec2_assign_role.png)
1. You will see the action of changing the EC2 instance IAM role occurring, which may take a several moments to complete.
![Cloud9 EC2 Instance - Assign Role Pending](./images/ec2_assign_role_processing.png)

1. Finally, you should see Success as shown below:
![Cloud9 EC2 Instance - Assign Role Pending](./images/ec2_assign_role_success.png)

### Congratulations, you have successfully configured Cloud9 for use in administering this workshop! Next, we will clone the repository with the workshop and labs.

## Clone Workshop Content - Cloud9

1. From the Getting Started panel on the right of the IDE, select **Clone Git Repository** and provide the URL of this repository (ie. https://github.com/zukoo/GG-Edge-Inference):
```
git clone https://github.com/zukoo/GG-Edge-Inference
```

1. We will also set up the environment for executing our code by entering the following in a shell prompt:
```
export PATH=/opt/c9/python3/bin:$PATH
pip3 install boto3
```

2. We will also need to configure the default region for our scripts -- within the shell, execute the following, using the \<region_name\> for your specific region:
```
aws configure
```
Your responses should look like the following, with your chosen region for the third prompt:
![Cloud9 Set AWS Region](./images/cloud9_region.png)

### Congratulations! We are now ready to begin Lab 1 activities on your Cloud9 environment.

## Clone Workshop Content - Local

1. Clone the workshop content to a local directory:
```
cd <your preferred scratch directory location>
git clone https://github.com/zukoo/GG-Edge-Inference
```

### Congratulations! We are now ready to begin Lab 1 activities in your local environment.

## Lab 1 Activities

1. From within the cloned directory, we will now switch to the directory for Lab 1 content and perform some necessary setup of our environment before we begin:
```
cd GG-Edge-Inference/
cd 1-greengrass-configuration/
```

1. Within this directory, we will use the `create-greengrass-config.py` script to generate the necessary groups for publishing our Greengrass function:

```
python3 create-greengrass-config.py --create-group ml-edge-workshop --bucket ml-edge-workshop-lab-1 --function ml-edge-workshop-lab-1
```
    
The above command is executed with the following parameters:
- **--create-group *\<group_name\>***: the group_name that will appear in your AWS IoT console referring to this device
- **--bucket *\<bucket_name\>***: the bucket_name of the Amazon S3 bucket you created earlier
- **--function *<function_name\>***: the function_name of the AWS Lambda function you created earlier

1. If successful, you should see similar output to the following:
![Greengrass certificates generated](./images/gg_certificates_generated.png)

1. *If using Cloud9*, you will need to download the certificates from the Lab 1 folder in the left-most project pane -- first select the `certificates.tar.gz` file with a single click, then left-clicking (Ctrl+Click on Mac OS X) to see the **Download** option as shown below:
![Cloud9 download](./images/cloud9_download.png)

## Install Certificates on Device

We will now install the AWS IoT certificates that we just created onto your local device

1. Download the `certificates.tar.gz` file from your Cloud9 instance, or locate it on your local drive.
1. Next, on the Jetson TX2 device, press the button **S3** or **REC** found on the edge of the board: ![Jetson TX2 buttons](./images/jetson_buttons.png)
1. Identify the device IP and connect to that IP on port 80/http with a web browser.![Jetson TX2 web config](./images/jetson_web_config.png)
1. In **Greengrass Certificates**, click **Choose File**, and select the `certificates.tar.gz` you had generated earlier, then click the **Finished**.
1. The device will display as follows, indicating device restart which is now occuring:
![Jetson TX2 web config](./images/jetson_restart.png)

## AWS IoT Connection
Now that the certificates are properly installed, we will attempt to confirm via the AWS Console:

1. From the AWS console, select IoT Core. We should see the AWS IoT Monitoring console as shown below, with a dot on the graph indicating a successful connection to our device.
![AWS IoT Core Monitor Success](./images/iot_monitor_success.png)

### You're now set to start doing some ML@Edge! Proceed to Lab 2

## Addendum: create-greengrass-config.py Usage

### Create Group

`python3 create-greengrass-config.py --create-group <GROUP_NAME> --bucket <BUCKET_NAME> --function <FUNCTION_NAME>`

### Delete Group

`python3 create-greengrass-config.py --delete-group`

### Get IP Address

`python3 create-greengrass-config.py --ip-address`
