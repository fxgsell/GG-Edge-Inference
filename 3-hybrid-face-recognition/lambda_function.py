import os
import boto3
import base64
import time
import json

REGION="us-east-1"
THRESHOLD=80

COLLECTION = os.environ['COLLECTION']
BUCKET = os.environ['BUCKET']
TABLE_NAME = os.environ['TABLE_NAME']

rekognition = boto3.client("rekognition", REGION)
dynamodb = boto3.resource('dynamodb')
iot = boto3.client('iot-data')
s3 = boto3.client('s3')

table = dynamodb.Table(TABLE_NAME)

collections = rekognition.list_collections()['CollectionIds'] 
print(collections)
if COLLECTION not in  collections :
    rekognition.create_collection(CollectionId=COLLECTION)

def lambda_handler(event, context):
    face = base64.b64decode(event['face'])
    thing = event['thing']

    file_name = 'face-'+time.strftime("%Y%m%d-%H%M%S")+'.jpg'
    print('s3://' + BUCKET + '/' + file_name)
    response = s3.put_object(Body=face, Bucket=BUCKET, Key=file_name)
    response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": BUCKET,
				"Name": file_name,
			}
		},
        CollectionId=COLLECTION
    )

    print("search_faces_by_image", response)
    if 'FaceMatches' in response and response['FaceMatches']:
        best = response['FaceMatches'][0]
        for match in response['FaceMatches']:
            if match['Similarity'] > best['Similarity']:
                best = match
        
        face_id = best['Face']['FaceId']
        response = table.get_item(
            Key={
                    'id': face_id
                }
        )
        if response['Item'] and 'name' in response['Item']:
            name = response['Item']['name']
        else:
            name = face_id[-5:]
    else:
        response = rekognition.index_faces(
            Image={
                "S3Object": {
                    "Bucket": BUCKET,
                    "Name": file_name,
                }
            },
            CollectionId=COLLECTION
        )
        face_id = response['FaceRecords'][0]['Face']['FaceId']
        table.put_item(
            Item={
                    'id': face_id,
                }
        )
        print("Indexing new face: ", face_id)
        name = face_id[-5:]


    topic = 'face_recognition/match/' + thing
    response = iot.publish(
        topic=topic,
        payload=json.dumps({event['id']: name})
    )
    print(response)