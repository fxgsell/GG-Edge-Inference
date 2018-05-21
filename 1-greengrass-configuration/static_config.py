import boto3

ROLE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetLifecycleConfiguration",
                "s3:ListBucketByTags",
                "s3:GetBucketTagging",
                "s3:GetInventoryConfiguration",
                "s3:GetObjectVersionTagging",
                "s3:GetBucketLogging",
                "s3:ListBucketVersions",
                "s3:GetAccelerateConfiguration",
                "s3:ListBucket",
                "s3:GetBucketPolicy",
                "s3:GetObjectAcl",
                "s3:GetObjectVersionTorrent",
                "s3:GetBucketRequestPayment",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetMetricsConfiguration",
                "s3:GetIpConfiguration",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketWebsite",
                "s3:GetBucketVersioning",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:GetReplicationConfiguration",
                "s3:ListMultipartUploadParts",
                "s3:GetObject",
                "s3:GetObjectTorrent",
                "s3:GetBucketCORS",
                "s3:GetAnalyticsConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::__BUCKET_NAME__"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:HeadBucket",
                "s3:ListObjects"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:log-group:*:*:*",
                "arn:aws:logs:*:*:log-group:/aws/greengrass*"
            ]
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        }
    ]
}

SUBSCRIPTION_INITIAL_VERSION = {
    'Subscriptions': [
        {
            'Source': 'function_arn',
            'Subject': '#',
            'Target': 'cloud'
        },
        {
            'Source': 'cloud',
            'Subject': '$aws/things/THING_NAME/shadow/update/accepted',
            'Target': 'function_arn'
        },
    ]
}

FUNCTION_INITIAL_VERSION = {
    'Functions': [
        {
            'FunctionConfiguration': {
                'Environment': {
                    'ResourceAccessPolicies': [
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-volume-shm'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-volume-tmp'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-gpu'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-ctrl'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-dbg-gpu'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-ctrl-gpu'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-prof-gpu'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvhost-vic'
                        },
                        {
                            'Permission': 'rw',
                            'ResourceId': 'data-device-nvmap'
                        }
                    ],
                    'AccessSysfs': True,
                    'Variables': {
                        'MXNET_CUDNN_AUTOTUNE_DEFAULT': '0',
                        'FULL_SIZE': '1',
                        'THING_NAME': ''
                    }
                },
                'Pinned': True,
                'EncodingType': 'json',
                'MemorySize': 6144000,
                'Timeout': 25
            },
            'FunctionArn': 'string',
            'Id': 'string'
        }
    ]
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
            "Id": "data-volume-shm",
            "Name": "shm",
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
                    "SourcePath": "/tmp",
                    "DestinationPath": "/tmp",
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


