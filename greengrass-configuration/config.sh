#!/bin/bash

REGION=us-east-1
GROUP_NAME=$1

echo "Creating " $GROUP_NAME "..."

CERTIFICATE_ID=$(aws iot create-keys-and-certificate --region $REGION --set-as-active \
                                                      --public-key-outfile public.key \
                                                      --certificate-pem-outfile cert.pem \
                                                      --private-key-outfile private.key \
                                                      --query certificateId \
                                                      --output text)

echo CERTIFICATE_ID=$CERTIFICATE_ID

CERTIFICATE_ARN=$(aws iot describe-certificate --certificate-id $CERTIFICATE_ID --query certificateDescription.certificateArn --output text)
echo CERTIFICATE_ARN=$CERTIFICATE_ARN

THING_ARN=$(aws iot create-thing --region $REGION --thing-name ${GROUP_NAME}_Core --query "thingArn" --output text)
echo THING_ARN=$THING_ARN

aws iot attach-thing-principal --region $REGION --thing-name ${GROUP_NAME}_Core --principal ${CERTIFICATE_ARN}

LOGGER_ARN=$(aws greengrass create-logger-definition --region $REGION --initial-version file://logger.json --output text --query "Arn")
echo LOGGER_ARN=$LOGGER_ARN

RESOURCES_ARN=$(aws greengrass create-resource-definition --region $REGION --cli-input-json file://resources.json --output text --query "Arn")
echo RESOURCES_ARN=$RESOURCES_ARN

SUBSCRIPTION_ARN=$(aws greengrass create-subscription-definition --region $REGION --initial-version file://subscription.json --output text --query "Arn")
echo SUBSCRIPTION_ARN=$SUBSCRIPTION_ARN

FUNCTION_ARN=$(aws greengrass create-function-definition --region $REGION --initial-version file://function.json --output text --query "Arn")
echo FUNCTION_ARN=$FUNCTION_ARN

DEVICE_ARN=$(aws greengrass create-device-definition --region $REGION --initial-version file://device.json --output text --query "Arn")
echo DEVICE_ARN=$DEVICE_ARN

GROUP_ID=$(aws greengrass create-group --region $REGION --name $GROUP_NAME --output text --query "Id")
echo=GROUP_ID=$GROUP_ID


CORE_ID=$(aws greengrass create-core-definition --name $GROUP_NAME_CoreDefinition --query Id --output text)
echo CORE_ID=$CORE_ID
CORE_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
CORE_ARN=$(aws greengrass create-core-definition-version --core-definition-id $CORE_ID --cores '[{"CertificateArn": "'$CERTIFICATE_ARN'", "ThingArn": "'$THING_ARN'", "SyncShadow": true, "Id": "'$CORE_ID'" }]' --query Arn --output text)
echo CORE_ARN=$CORE_ARN



aws greengrass create-group-version --group-id $GROUP_ID --region $REGION \
                                    --core-definition-version-arn $CORE_ARN \
                                    --device-definition-version-arn $DEVICE_ARN \
                                    --function-definition-version-arn $FUNCTION_ARN \
                                    --logger-definition-version-arn $LOGGER_ARN \
                                    --resource-definition-version-arn $RESOURCES_ARN \
                                    --subscription-definition-version-arn $SUBSCRIPTION_ARN

echo Deleting everything
aws greengrass delete-group --group-id $GROUP_ID

aws iot detach-thing-principal --thing-name $1_Core --principal $CERTIFICATE_ARN
aws iot update-certificate --new-status INACTIVE --certificate-id $CERTIFICATE_ID 
aws iot delete-certificate --certificate-id $CERTIFICATE_ID 
aws iot delete-thing --thing-name $1_Core 


exit

### CONFIG BUILD ### TODO
ID=${CERTIFICATE_ARN: -11}
ID=${ID:0:10}
echo $ID

mkdir config
mkdir certs

mv private.key certs/$ID.private.key
mv public.key certs/$ID.public.key 
mv cert.pem certs/$ID.cert.pem

cp config.template.json config/config.json

sed -i 's/__CERT__/'$ID'\.cert\.pem/g' config.json
sed -i 's/__KEY__/'$ID'\.private\.key/g' config.json
sed -i 's/__THING_ARN__/'$THING_ARN'/g' config.json

zip -r configuration.zip config certs

rm -r keys
rm -r config
