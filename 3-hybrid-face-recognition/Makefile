TEMPLATE=hybrid-face-recognition.yml
FINAL_TEMPLATE=hybrid-face-recognition-release.yml
CF_STACK=Hybrid-Face-Recognition

include ../properties.mk

all: build deploy

build:
	make -C function
	aws cloudformation package \
		--template-file $(TEMPLATE) \
		--s3-bucket $(BUCKET) \
		--output-template-file $(FINAL_TEMPLATE)

deploy: all
	aws cloudformation deploy \
		--region $(REGION) \
		--template-file $(FINAL_TEMPLATE) \
		--stack-name $(CF_STACK) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides 'BucketName=$(BUCKET)'

