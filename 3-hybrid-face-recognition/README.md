# Hybrid Face recognition between Cloud and Edge

Now we have a very basic face detection and recognition model running on the device. This model is capable of remembering the last faces it has seen but this is very limited. We can store a much more complete database of faces in and Amazon Rekognition and use it to label the new faces. Because the device itself is capable of running a part oof the inference we can have considerably cheaper and Amazon Rekognition costs that we would have if we were streaming all the images to it, this will also improve the latency for the faces that have already been identified recently.

![Architecture][architecture]

[architecture]: ./static/architecture.png "Architecture"

## Step-by-step

- You can reuse the same lambda as in the first section, or create a new one (with the same alias latest). If you choose to create a new one you must add it to you Greengrass group with 'python3 create-greengrass-config --function <YOUR_FUNCTION>.

- Create another Lambda function which will be using Rekognition to resolve the name of the faces it receive, only create it in the cloud this time.

- In Amazon Rekognition create a pool of face that you need to identify.

- Edit the code to crop the Faces which have not been identified yet, and send them to recognition for identification.
    1. Send the message to a topic. 'jetson/new_faces'
    2. Lambda subscribe to the topic.
    3. When the lambda receive a new face.
        - Save it in S3,
        - Send it to Rekognition:
            - If Rekognition knows it: Lookup the ID In DynamoDB, add the ID -> Name in the shadow of the device.
            - Else add it to the pool, and save it in DynamoDB.
    4. Populate the DynamoDB table with a few names.

- When you get a shadow update edit the key of the know face.

After that you should see the name of the person that you configured in recognition instead of "UserXYZ".

## Tips

- Crop a photo in Python with cv2 : `crop = frame[y:y+h, x:x+w]`

- Create a face pool in Rekognition:
