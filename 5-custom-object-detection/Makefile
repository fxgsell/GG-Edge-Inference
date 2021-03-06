include ../properties.mk

GG_DEPS=greengrass_common  greengrass_ipc_python_sdk  greengrasssdk
DEPS=symbol
STATUS=$(AWS_COMMAND) greengrass get-deployment-status --group-id `cat GROUP_ID` --deployment-id `cat GROUP_DEPLOYMENT` --query "DeploymentStatus" --output text
all: publish

build:
	echo "Zipping..."
	rm -f package.zip
	zip -rq package.zip $(GG_DEPS) $(DEPS) *.py

deploy: build
	echo "Uploading to Lambda"
	$(AWS_COMMAND) lambda update-function-code --function-name $(LAMBDA_FUNCTION) --zip-file fileb://`pwd`/package.zip
	$(AWS_COMMAND) lambda publish-version --function-name $(LAMBDA_FUNCTION) --query Version --output text  > LAMBDA_VERSION
	$(AWS_COMMAND) lambda update-alias --name $(LAMBDA_ALIAS) --function-name $(LAMBDA_FUNCTION) --function-version `cat LAMBDA_VERSION`
	rm LAMBDA_VERSION

publish: deploy
	echo "Deploying to GG"
	$(AWS_COMMAND) greengrass list-groups --query "Groups[?Name=='$(GG_GROUP)'].Id" --output text > GROUP_ID
	$(AWS_COMMAND) greengrass list-groups --query "Groups[?Name=='$(GG_GROUP)'].LatestVersion" --output text > GROUP_VERSION
	$(AWS_COMMAND) greengrass create-deployment --group-id `cat GROUP_ID` --deployment-type NewDeployment --group-version-id `cat GROUP_VERSION` --query "DeploymentId" --output text > GROUP_DEPLOYMENT
	$(AWS_COMMAND) greengrass get-deployment-status --group-id `cat GROUP_ID` --deployment-id `cat GROUP_DEPLOYMENT` --query "DeploymentStatus" --output text  > STATUS
	@echo "Build in progress:" `cat STATUS`
	until $(STATUS) | tee STATUS | grep -w -v -m 1 "Building\|InProgress"; do sleep 1 ; done
    @echo "Finished:" `cat STATUS`
	rm GROUP_ID GROUP_VERSION GROUP_DEPLOYMENT STATUS
