import boto3

FUNCTION_INITIAL_VERSION = { ### TODO
    "Name": "MyFunctionDefinition",
    "InitialVersion": {
        "Functions": [
            {
                "Id": "greengrassLraTest",
                "FunctionArn": "arn:aws:lambda:us-west-2:012345678901:function:lraTest:1",
                "FunctionConfiguration": {
                    "Pinned": False,
                    "MemorySize": 16384,
                    "Timeout": 30,
                    "Environment": {
                        "ResourceAccessPolicies": [
                            {
                                "ResourceId": "data-volume",
                                "Permission": "rw"
                            },
                            {
                                "ResourceId": "data-device",
                                "Permission": "ro"
                            }                            
                        ],
                        "AccessSysfs": True
                    }
                }
            }
        ]
    }
}

CONFIG_FILE = {
    "coreThing" : {
        "caPath" : "root.ca.pem",
        "certPath" : "__CERT__",
        "keyPath" : "__PRIV_KEY__",
        "thingArn" : "__THING_ARN__",
        "iotHost" : "aq7sp3lvaf0b7.iot.us-east-1.amazonaws.com",
        "ggHost" : "greengrass.iot.us-east-1.amazonaws.com",
        "keepAlive" : 600
    },
    "runtime" : {
        "cgroup" : {
        "useSystemd" : "yes"
        }
    },
    "managedRespawn" : False
}

CORE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["iot:Publish", "iot:Subscribe", "iot:Connect", "iot:Receive", "iot:GetThingShadow", "iot:DeleteThingShadow", "iot:UpdateThingShadow"],
            "Resource": ["arn:aws:iot:" + boto3.session.Session().region_name + ":*:*"]
        },
        {
            "Effect": "Allow",
            "Action": ["greengrass:AssumeRoleForGroup", "greengrass:CreateCertificate", "greengrass:GetConnectivityInfo", "greengrass:GetDeployment", "greengrass:GetDeploymentArtifacts", "greengrass:UpdateConnectivityInfo", "greengrass:UpdateCoreDeploymentStatus"],
            "Resource": ["*"]
        }
    ]
}


LOGGER_INITIAL_VERSION = {
    "Loggers": [
        {
          "Component": "Lambda",
          "Id": "local-lambda",
          "Level": "INFO",
          "Space": 25,
          "Type": "FileSystem"
        },
        {
          "Component": "GreengrassSystem",
          "Id": "local-system",
          "Level": "INFO",
          "Space": 25,
          "Type": "FileSystem"
        },
        {
          "Component": "Lambda",
          "Id": "cloudwatch-lambda",
          "Level": "INFO",
          "Type": "AWSCloudWatch"
        },
        {
          "Component": "GreengrassSystem",
          "Id": "cloudwatch-system",
          "Level": "INFO",
          "Type": "AWSCloudWatch"
        }
    ]
  }




RESOURCE_INITIAL_VERSION = {
    "Resources": [
        {
            "Id": "shm",
            "Name": "data-volume-shm",
            "ResourceDataContainer": {
                "LocalVolumeResourceData": {
                    "SourcePath": "/dev/shm",
                    "DestinationPath": "/dev/shm",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-volume-tmp",
            "Name": "tmp",
            "ResourceDataContainer": {
                "LocalVolumeResourceData": {
                    "SourcePath": "/dev/tmp",
                    "DestinationPath": "/dev/tmp",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-gpu",
            "Name": "nvhost-gpu",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-gpu",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-ctrl",
            "Name": "nvhost-ctrl",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-ctrl",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-dbg-gpu",
            "Name": "nvhost-dbg-gpu",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-dbg-gpu",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-ctrl-gpu",
            "Name": "nvhost-ctrl-gpu",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-ctrl-gpu",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-prof-gpu",
            "Name": "nvhost-prof-gpu",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-prof-gpu",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvhost-vic",
            "Name": "nvhost-vic",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvhost-vic",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        },
        {
            "Id": "data-device-nvmap",
            "Name": "nvmap",
            "ResourceDataContainer": {
                "LocalDeviceResourceData": {
                    "SourcePath": "/dev/nvmap",
                    "GroupOwnerSetting": {
                        "AutoAddGroupOwner": True
                    }
                }
            }
        }
    ]
}


