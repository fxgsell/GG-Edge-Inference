import boto3
import uuid
import static_config
import json
import argparse
import os
import shutil
import datetime

greengrass = boto3.client('greengrass')
iot = boto3.client('iot')
iam = boto3.client('iam')

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def remove_assets(state):
    ''' Load the status and delete all ressources'''
    print("Removing assets.")

    try: greengrass.reset_deployments(Force=True, GroupId=state['group']['Id'])
    except: pass
    try: greengrass.delete_group(GroupId=state['group']['Id'])
    except: pass
    try: greengrass.delete_logger_definition(LoggerDefinitionId=state['logger']['Id'])
    except: pass
    try: greengrass.delete_core_definition(CoreDefinitionId=state['core_definition']['Id'])
    except: pass
    try: greengrass.delete_resource_definition(ResourceDefinitionId=state['resource']['Id'])
    except: pass

    if 'function' in state:
        try: greengrass.delete_function_definition(FunctionDefinitionId=state['function']['Id'])
        except: pass
    if 'subscription' in state:
        try: greengrass.delete_subscription_definition(SubscriptionDefinitionId=state['subscription']['Id'])
        except: pass

    try: iot.detach_thing_principal(thingName=state['core_thing']['thingName'],
        principal=state['keys_cert']['certificateArn'])
    except: pass
    try: iot.update_certificate(certificateId=state['keys_cert']['certificateId'],
        newStatus='INACTIVE')
    except: pass
    try: iot.detach_principal_policy(policyName=state['policy']['policyName'],
        principal=state['keys_cert']['certificateArn'])
    except: pass
    try: iot.delete_certificate(certificateId=state['keys_cert']['certificateId'])
    except: pass

    try: iot.delete_policy(policyName=state['policy']['policyName'])
    except: pass
    try: iot.delete_thing(thingName=state['core_thing']['thingName'])
    except: pass

    try: iam.detach_role_policy(RoleName=state['role']['Role']['RoleName'],
        PolicyArn=state['role_policy']['Policy']['Arn'])
    except: pass
    try: iam.delete_policy(PolicyArn=state['role_policy']['Policy']['Arn'])
    except: pass
    try: iam.delete_role(RoleName=state['role']['Role']['RoleName'])
    except: pass


def generate_config_package(state):
    print("Generating configuration package")
    package_id = state['keys_cert']['certificateArn'][-10:]

    config = static_config.CONFIG_FILE
    config["coreThing"]["certPath"] = package_id+'.cert.pem'
    config["coreThing"]["keyPath"] = package_id+'.private.key'
    config["coreThing"]["thingArn"] = state['core_thing']['thingArn']
    config["coreThing"]["iotHost"] = iot.describe_endpoint()['endpointAddress']

    shutil.rmtree( './artifacts', True)
    if os.path.isfile('certificates.zip'):
        os.remove('certificates.zip')

    os.mkdir('./artifacts')
    os.mkdir('./artifacts/certs')
    os.mkdir('./artifacts/config')

    with open('./artifacts/config/config.json', 'w') as f:
        json.dump(config, f, indent=4)
        f.close()

    with open('./artifacts/certs/'+config["coreThing"]["certPath"], 'w') as f:
        f.write(state['keys_cert']['certificatePem'])
        f.close()

    with open('./artifacts/certs/'+config["coreThing"]["keyPath"], 'w') as f:
        f.write(state['keys_cert']['keyPair']['PrivateKey'])
        f.close()

    with open('./artifacts/certs/'+package_id+'.public.key', 'w') as f:
        f.write(state['keys_cert']['keyPair']['PublicKey'])
        f.close()

    shutil.make_archive('certificates', 'gztar', './artifacts/', '.')
    shutil.rmtree( './artifacts')
    print('Configuration and certificates generated: certificates.zip')

def create_function(): #TODO
    return 

def create_gg_role(bucket_name, id):
    print("Creating IAM role for Greengrass")
    document = static_config.ROLE_POLICY
    assume_role_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "greengrass.amazonaws.com"
                }
            }
        ]
    }

    role = iam.create_role(
        RoleName='GG_Edge_Inference_Role_'+id,
        AssumeRolePolicyDocument=json.dumps(assume_role_document)
    )
    document['Statement'][0]["Resource"] = document['Statement'][0]["Resource"] + bucket_name
    policy = iam.create_policy(
        PolicyName='GG_Edge_Inference_Policy_'+id,
        PolicyDocument=json.dumps(document),
        Description='Grant access to cloud watch and an s3 bucket'
    )
    iam.attach_role_policy(
        RoleName=role['Role']['RoleName'],
        PolicyArn=policy['Policy']['Arn']
    )
    return role, policy

def create_group(group_name, bucket):
    thing_name = group_name+'_Core'
    certificate = iot.create_keys_and_certificate(setAsActive=True)
    thing = iot.create_thing(thingName=thing_name)

    iot.attach_thing_principal(
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

    group = greengrass.create_group(
        InitialVersion={
            'CoreDefinitionVersionArn': core['LatestVersionArn'],
            'LoggerDefinitionVersionArn': logger['LatestVersionArn'],
            'ResourceDefinitionVersionArn': resource['LatestVersionArn']},
        Name=group_name
    )

    role, role_policy = create_gg_role(bucket, certificate['certificateArn'][-10:])
    greengrass.associate_role_to_group(
        GroupId=group['Id'],
        RoleArn=role['Role']['Arn']
    )

    state = {
        'id': certificate['certificateArn'][-10:],
        'name': thing_name,
        'role': role,
        'role_policy': role_policy,
        'group': group,
        'core_thing': thing,
        'keys_cert': certificate,
        'resource': resource,
        'logger': logger,
        'core_definition': core,
        'policy': policy
    }

    return state

def add_function(name, state):

    client = boto3.client('lambda')   
    lambda_function = client.get_function(FunctionName=name)
    arn = lambda_function['Configuration']['FunctionArn']+":latest"
    function = static_config.FUNCTION_FACE_INITIAL_VERSION 
    function['Functions'][0]['FunctionArn'] = arn
    function['Functions'][0]['Id'] = str(uuid.uuid1())
    function['Functions'][0]['FunctionConfiguration']['Environment']['Variables']['THING_NAME'] = state['name']

    response = greengrass.create_function_definition(InitialVersion=function)
    state['function'] = response

    subscription = static_config.SUBSCRIPTION_INITIAL_VERSION 
    subscription['Subscriptions'][0]['Target'] = arn
    subscription['Subscriptions'][0]['Subject'] = 'face_recognition/match/' + state['name']
    subscription['Subscriptions'][0]['Id'] = str(uuid.uuid1())

    subscription['Subscriptions'][1]['Source'] = arn
    subscription['Subscriptions'][1]['Id'] = str(uuid.uuid1())

    subscription['Subscriptions'][2]['Source'] = arn
    subscription['Subscriptions'][2]['Id'] = str(uuid.uuid1())

    subscription['Subscriptions'][3]['Source'] = arn
    subscription['Subscriptions'][3]['Id'] = str(uuid.uuid1())
    
    response = greengrass.create_subscription_definition(
        InitialVersion=subscription
    )
    state['subscription'] = response

    response = greengrass.create_group_version(
        CoreDefinitionVersionArn=state['core_definition']['LatestVersionArn'],
        FunctionDefinitionVersionArn=state['function']['LatestVersionArn'],
        GroupId=state['group']['Id'],
        LoggerDefinitionVersionArn=state['logger']['LatestVersionArn'],
        ResourceDefinitionVersionArn=state['resource']['LatestVersionArn'],
        SubscriptionDefinitionVersionArn=state['subscription']['LatestVersionArn']
    )
    return state

def get_connectivity():
    with open('./state.json', 'r') as f:
        state = json.load(f)
        response = greengrass.get_connectivity_info(ThingName=state['core_thing']['thingName'])
        response.pop('ResponseMetadata', None)
        for val in response['ConnectivityInfo']:
            ip = val['HostAddress']
            if ":" not in ip and ip != '127.0.0.1':
                print(val['HostAddress'])
            

### ENTRY POINT ###

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--create-group', dest='group_name', action='store',
                   default='',
                   help='Create a new Greengrass Group With the specified Name')
parser.add_argument('--bucket', dest='bucket', action='store',
                   default='',
                   help='Specify the ML models bucket name')
parser.add_argument('--delete-group', dest='delete_group', action='store_true',
                   default=False, 
                   help='Delete resources in the state file specified')
parser.add_argument('--state-file', dest='state_file', action='store',
                   help='Specify a state file')
parser.add_argument('--ip-address', dest='ip_address', action='store_true',
                   default=False, 
                   help='Get greengrass core ip address')
parser.add_argument('--function', dest='function_name', action='store',
                   help='Create a lambda in the group with the specified name')

args = parser.parse_args()
state = None

if args.delete_group:
    if args.state_file is None:
        print("Please specify a state file with --state-file.")
        exit(1)
    state_file = args.state_file
    with open(state_file, 'r') as f:
        state = json.load(f)
        remove_assets(state)
        os.remove(state_file) 
elif args.ip_address:
    get_connectivity()
elif args.group_name != "" and args.bucket == "":
    print("Please specify a bucket with --bucket BUCKET_NAME")
elif args.group_name != "":
    state = create_group(args.group_name, args.bucket)
    state_file = './state_'+state['id']+'.json'

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4, default = dateconverter)
        f.close()
    generate_config_package(state)

if args.function_name is not None:
    if state is None and args.state_file is None:
        print("Please specify a state file with --state-file.")
        exit(1)
    elif state is None:
        state_file = args.state_file
        with open(state_file, 'r') as f:
            state = json.load(f)

    state = add_function(args.function_name, state)
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4, default = dateconverter)
        f.close()
    ## TODO: Generate Makefile.parameters

    print("Resources created, install the package on your device.")
