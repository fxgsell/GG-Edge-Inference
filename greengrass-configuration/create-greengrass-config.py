import boto3
import uuid
import static_config
import json
import argparse
import os

greengrass = boto3.client('greengrass')
iot = boto3.client('iot')

def remove_assets():
    ''' Load the status and delete all ressources'''
    print("Removing assets:")
    with open('./state.json', 'r') as f:
        state = json.load(f)

        greengrass.delete_group(GroupId=state['group']['Id'])
        greengrass.delete_logger_definition(LoggerDefinitionId=state['logger']['Id'])
        greengrass.delete_core_definition(CoreDefinitionId=state['core_definition']['Id'])
        greengrass.delete_resource_definition(ResourceDefinitionId=state['resource']['Id'])

        iot.detach_thing_principal(thingName=state['core_thing']['thingName'], principal=state['keys_cert']['certificateArn'])
        iot.update_certificate(certificateId=state['keys_cert']['certificateId'], newStatus='INACTIVE')

        iot.detach_principal_policy(policyName=state['policy']['policyName'],
            principal=state['keys_cert']['certificateArn'])
        iot.delete_certificate(certificateId=state['keys_cert']['certificateId'])

        iot.delete_policy(policyName=state['policy']['policyName'])
        iot.delete_thing(thingName=state['core_thing']['thingName'])

        f.close()
        os.remove('./state.json') 


def create_group(group_name):
    thing_name = group_name+'_Core'
    certificate = iot.create_keys_and_certificate(setAsActive=True)
    thing = iot.create_thing(thingName=thing_name)

    response = iot.attach_thing_principal(
        thingName=thing_name,
        principal=certificate['certificateArn']
    )

    policy = iot.create_policy(
        policyName=group_name+"_policy",
        policyDocument=json.dumps(static_config.CORE_POLICY))

    iot.attach_principal_policy(
        policyName=policy['policyName'],
        principal=certificate['certificateArn'])

    core = greengrass.create_core_definition(
        InitialVersion={
            'Cores': [
                {
                    'CertificateArn': certificate['certificateArn'],
                    'Id': str(uuid.uuid1()),
                    'SyncShadow': True,
                    'ThingArn': thing['thingArn']
                },
            ]
        },
        Name=group_name+'_Core'
    )

    logger = greengrass.create_logger_definition(InitialVersion=static_config.LOGGER_INITIAL_VERSION)

    resource = greengrass.create_resource_definition(InitialVersion=static_config.RESOURCE_INITIAL_VERSION)
    #print(resource)

    group = greengrass.create_group(
        InitialVersion={
            'CoreDefinitionVersionArn': core['LatestVersionArn'],
            'LoggerDefinitionVersionArn': logger['LatestVersionArn'],
            'ResourceDefinitionVersionArn': resource['LatestVersionArn']
        },
        Name=group_name
    )
    print(response)

    #TODO For logstash and ML: No role has been attached to the WORKSHOP_JETSON Group

    state = {
        'group': group,
        'core_thing': thing,
        'keys_cert': certificate,
        'resource': resource,
        'logger': logger,
        'core_definition': core,
        'policy': policy
    }
        
    with open('./state.json', 'w') as f:
        json.dump(state, f, indent=4)

 #################
### ENTRY POINT ###
 #################

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--create-group', dest='group_name', action='store',
                   default='JETSON_WORKSHOP',
                   help='Create a new Greengrass Group With the specified Name')
parser.add_argument('--delete-group', dest='delete_group', action='store_true',
                   default=False, 
                   help='Create a new Greengrass Group With the specified Name')

args = parser.parse_args()

if args.delete_group:
    remove_assets()
elif args.group_name != "":
    create_group(args.group_name)