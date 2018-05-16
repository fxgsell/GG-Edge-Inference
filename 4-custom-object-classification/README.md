# Create you own model for inference at the Edge

## Steps

1. Create a SageMaker notebook, and upload [notebook.jpny](./notebook.jpny). Follow the steps in the notebook after which you should have a working model.

1. In the IOT console add a ML Resource to your Greengras Group. Choose the resource destination path for the model and also add it as an env variable for the Lambda `ML_PATH`.

1. Still in the IOT console add an env variable `BUCKET` with the bucket name to the lamnda function.

1. Run `make` and wait for it (the device must download the model so it might be slower than in the previous sections).

## Extra Work

- Use SageMaker's object detection algorithm to implement real time boxing of the objects.