# Create you own model for inference at the Edge

## Steps

1. Create a SageMaker notebook, and upload [Image-classification-fulltraining.ipynb](./Image-classification-fulltraining.ipynb). Follow the steps in the notebook after which you should have a working model.

1. In the IOT console add a ML Resource to your Greengrass Group. Choose the resource destination path for the model and also add it as an env variable for the Lambda `ML_PATH`.
    ![Add model](./images/add_model.png)

1. In the greengrass group create a new subscription which allows your lambda to post to the topics `custom_object_detection/#`.
    ![Subscriptions configurations](./images/subscriptions.png)

1. Run `make` and wait for it (the device must download the model so it might be slower than in the previous sections).

1. Subscribe to the topics `custom_object_detection/admin` and `custom_object_detection/inference` or to `custom_object_detection/#` to see the inference.
