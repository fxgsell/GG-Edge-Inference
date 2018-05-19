# Hybrid Face recognition between Cloud and Edge

Now we have a very basic face detection and recognition model running on the device. This model is capable of remembering the last faces it has seen but this is very limited. We can store a much more complete database of faces in and Amazon Rekognition and use it to label the new faces. Because the device itself is capable of running a part oof the inference we can have considerably cheaper and Amazon Rekognition costs that we would have if we were streaming all the images to it, this will also improve the latency for the faces that have already been identified recently.

![Architecture][architecture]

[architecture]: ./static/architecture.png "Architecture"

## Step-by-step

- In Amazon Rekognition create a pool of face that you need to identify.

- Edit the code to crop the Faces which have not been identified yet, and send them to recognition for identification.

- When you get the response update the face name.

After that you should see the name of the person that you configured in recognition instead of "UserXYZ".

## Tips

- Crop a photo in Python with cv2 : `crop = frame[y:y+h, x:x+w]`

- Create a face pool in Rekognition: 
