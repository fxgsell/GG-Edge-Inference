#!/bin/bash

REGION=us-east-1
GROUP_NAME=$1

aws greengrass --region $REGION --list-resource-definitions