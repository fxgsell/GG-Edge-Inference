import os
import boto3
import base64
import time
import json

COLLECTION = os.environ['COLLECTION']
BUCKET = os.environ['BUCKET']
REGION="us-east-1"
THRESHOLD=80
TABLE_NAME = 'face-table'

rekognition = boto3.client("rekognition", REGION)
dynamodb = boto3.resource('dynamodb')
iot = boto3.client('iot-data')

table = dynamodb.Table(TABLE_NAME)

if COLLECTION not in rekognition.list_collections():
    rekognition.create_collection(CollectionId=COLLECTION)

def lambda_handler(event, context):
    BUCKET = "fx-dl-faces"
    face = base64.b64decode(event['face'])
    s3 = boto3.client('s3')
    thing = event['thing']
    shadow = { "state": { "desired": {} } }
    # shadow['state']['desired'][event['id']] = XYZ

    file_name = 'face-'+time.strftime("%Y%m%d-%H%M%S")+'.jpg'
    response = s3.put_object(ACL='public-read', Body=face, Bucket=BUCKET, Key=file_name)
    print(response)
    response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": BUCKET,
				"Name": file_name,
			}
		},
        CollectionId=COLLECTION,
        FaceMatchThreshold=THRESHOLD,
    )

    if response['FaceRecords']:
        best = response['FaceRecords'][0]
        for match in response['FaceRecords']:
            if match['Similarity'] > best['Similarity']:
                best = match
        
        response = table.get_item(
            Key={
                    'id': best['FaceId']
                }
        )
        if response['Item'] and response['Item']['name']:
            shadow['state']['desired'][event['id']] = response['Item']['name']
        else:
            shadow['state']['desired'][event['id']] = best['FaceId'][:-5]
    else:
        response = rekognition.index_faces(
            Image={
                "S3Object": {
                    "Bucket": BUCKET,
                    "Name": file_name,
                }
            },
            CollectionId=COLLECTION,
            ExternalImageId=None,
            DetectionAttributes=(),
        )

        table.put_item(
            Item={
                    'id': response['FaceRecords'][0]['FaceId'],
                }
        )
        print("Indexing new face: ", response['FaceRecords'][0]['FaceId'])
        shadow['state']['desired'][event['id']] = response['FaceRecords'][0]['FaceId'][:-5]

    response = iot.update_thing_shadow(
        thingName=thing,
        payload=json.dumps(shadow),
    )