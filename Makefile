.PHONY: requirements

LAMBDA_AND_CONTAINER_NAME = hello-lambda
AWS_REGION = us-west-1
ACCOUNT_ID = 212263820079
ECR_URI = $(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
AWS_DOCKERFILE_NAME = Dockerfile.aws.lambda

create_environment:
	conda create --yes --name $(LAMBDA_AND_CONTAINER_NAME) python=3.8

requirements:
	pip install -r requirements-dev.txt

build_image:
	docker build -t $(LAMBDA_AND_CONTAINER_NAME) . --file $(AWS_DOCKERFILE_NAME)

authenticate_ecr:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URI)

create_ecr_repository: authenticate_ecr
	aws ecr create-repository --repository-name $(LAMBDA_AND_CONTAINER_NAME) --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

deploy_to_ecr: build_image authenticate_ecr
	docker tag  $(LAMBDA_AND_CONTAINER_NAME):latest $(ECR_URI)/$(LAMBDA_AND_CONTAINER_NAME):latest
	docker push $(ECR_URI)/$(LAMBDA_AND_CONTAINER_NAME):latest
