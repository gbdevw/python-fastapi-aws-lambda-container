### Archived

This repository has been archived and will no longer be supported.

### Python + FastAPI + Mangum + AWS Lambda Container

A demo project to test the AWS Lambda container support with Python FastAPI framework. The purpose of the project is to show how to develop a REST API with FastAPI, how to build & test it locally and how to deploy it on AWS using serverless services (AWS ECR, AWS Lambda & AWS API Gateway).

### Prerequisites

- Docker CLI
- Python 3.8

### Install dependencies

A requirements file declare all dependencies (Mangum, FastAPI, Uvicorn, ...). Use the following command to install the required dependencies (For Python 3.8.5)

```
pip install -r ./requirements.txt
```

TIP : Before installing required dependencies, do not forget to create a virtual environment using your favorite tool (Conda, ...).

### Run locally

You can either use the following command :

```
python -m app.app
```

Or deploy on uvicorn :

```
uvicorn app.app:app --reload --host 0.0.0.0 --port 5000
```

You can test the application by using the following command : 

```
curl http://localhost:5000/hello/
```

### Build the 'regular' container

This command builds a container which will run a Uvicorn server and deploy the ASGI app on it : 

```
docker build -t hello-world-uvicorn . 
```

### Run the container

The command starts the container :

```
docker run -p 5000:5000 hello-world-uvicorn:latest
```

You can make a test with this command :

```
curl http://localhost:5000/hello/
```

### Build the container for AWS Lambda

Now we can build the container for AWS Lambda which will use the Mangum handler. We use another Dockerfile which will use a base image provided by AWS :

```
docker build -t hello-world-lambda . -f Dockerfile.aws.lambda
```

### Run the AWS Lambda container for local test

Let's start the container to test the lambda locally :

```
docker run -p 9000:8080 hello-world-lambda:latest
```

### Test the Lambda

We send the input event that the lambda would receive from the API Gateway with the following command :

```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
    "resource": "/hello",
    "path": "/hello/",
    "httpMethod": "GET",
    "headers": {
      "Accept": "*/*",
      "Accept-Encoding": "gzip, deflate",
      "cache-control": "no-cache",
      "CloudFront-Forwarded-Proto": "https",
      "CloudFront-Is-Desktop-Viewer": "true",
      "CloudFront-Is-Mobile-Viewer": "false",
      "CloudFront-Is-SmartTV-Viewer": "false",
      "CloudFront-Is-Tablet-Viewer": "false",
      "CloudFront-Viewer-Country": "US",
      "Content-Type": "application/json",
      "headerName": "headerValue",
      "Host": "gy415nuibc.execute-api.us-east-1.amazonaws.com",
      "Postman-Token": "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f",
      "User-Agent": "PostmanRuntime/2.4.5",
      "Via": "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)",
      "X-Amz-Cf-Id": "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==",
      "X-Forwarded-For": "54.240.196.186, 54.182.214.83",
      "X-Forwarded-Port": "443",
      "X-Forwarded-Proto": "https"
    },
    "multiValueHeaders":{
      "Accept":[
        "*/*"
      ],
      "Accept-Encoding":[
        "gzip, deflate"
      ],
      "cache-control":[
        "no-cache"
      ],
      "CloudFront-Forwarded-Proto":[
        "https"
      ],
      "CloudFront-Is-Desktop-Viewer":[
        "true"
      ],
      "CloudFront-Is-Mobile-Viewer":[
        "false"
      ],
      "CloudFront-Is-SmartTV-Viewer":[
        "false"
      ],
      "CloudFront-Is-Tablet-Viewer":[
        "false"
      ],
      "CloudFront-Viewer-Country":[
        "US"
      ],
      "":[
        ""
      ],
      "Content-Type":[
        "application/json"
      ],
      "headerName":[
        "headerValue"
      ],
      "Host":[
        "gy415nuibc.execute-api.us-east-1.amazonaws.com"
      ],
      "Postman-Token":[
        "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f"
      ],
      "User-Agent":[
        "PostmanRuntime/2.4.5"
      ],
      "Via":[
        "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)"
      ],
      "X-Amz-Cf-Id":[
        "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A=="
      ],
      "X-Forwarded-For":[
        "54.240.196.186, 54.182.214.83"
      ],
      "X-Forwarded-Port":[
        "443"
      ],
      "X-Forwarded-Proto":[
        "https"
      ]
    },
    "queryStringParameters": {
    },
    "multiValueQueryStringParameters":{
    },
    "pathParameters": {
    },
    "stageVariables": {
      "stageVariableName": "stageVariableValue"
    },
    "requestContext": {
      "accountId": "12345678912",
      "resourceId": "roq9wj",
      "stage": "testStage",
      "requestId": "deef4878-7910-11e6-8f14-25afc3e9ae33",
      "identity": {
        "cognitoIdentityPoolId": null,
        "accountId": null,
        "cognitoIdentityId": null,
        "caller": null,
        "apiKey": null,
        "sourceIp": "192.168.196.186",
        "cognitoAuthenticationType": null,
        "cognitoAuthenticationProvider": null,
        "userArn": null,
        "userAgent": "PostmanRuntime/2.4.5",
        "user": null
      },
      "resourcePath": "/hello/",
      "httpMethod": "GET",
      "apiId": "gy415nuibc"
    },
    "body": "{}",
    "isBase64Encoded": false
}'
```

See the server logs :
```
(fastapi-lambda-container) gbdevw@gbdevw-dev:~/python-fastapi-aws-lambda-container$ docker run -p 9000:8080 hello-world:latest
time="2020-12-28T15:31:13.892" level=info msg="exec '/var/runtime/bootstrap' (cwd=/var/task, handler=)"
time="2020-12-28T15:31:18.345" level=info msg="extensionsDisabledByLayer(/opt/disable-extensions-jwigqn8j) -> stat /opt/disable-extensions-jwigqn8j: no such file or directory"
time="2020-12-28T15:31:18.345" level=warning msg="Cannot list external agents" error="open /opt/extensions: no such file or directory"
START RequestId: b7cd3c8d-6c70-4194-b5bd-6a0b8e766b1f Version: $LATEST
{"timestamp": "2020-12-28T15:31:18.650259", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "Waiting for application startup."}
{"timestamp": "2020-12-28T15:31:18.650726", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "LifespanCycleState.STARTUP:  'lifespan.startup.complete' event received from application."}
{"timestamp": "2020-12-28T15:31:18.650863", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "Application startup complete."}
{"timestamp": "2020-12-28T15:31:18.651481", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "api-request", "message": "Request", "uuid": "bd8ec07d-2b70-436d-8157-1d802be13240", "method": "GET", "url": "https://gy415nuibc.execute-api.us-east-1.amazonaws.com/hello/"}
{"timestamp": "2020-12-28T15:31:18.652105", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "api-response", "message": "Response sent", "uuid": "bd8ec07d-2b70-436d-8157-1d802be13240", "code": 200}
{"timestamp": "2020-12-28T15:31:18.652506", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "HTTPCycleState.REQUEST:  'http.response.start' event received from application."}
{"timestamp": "2020-12-28T15:31:18.652641", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "HTTPCycleState.RESPONSE:  'http.response.body' event received from application."}
{"timestamp": "2020-12-28T15:31:18.652750", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "HTTPCycleState.RESPONSE:  'http.response.body' event received from application."}
{"timestamp": "2020-12-28T15:31:18.652996", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "HTTPCycleState.RESPONSE:  'http.response.body' event received from application."}
{"timestamp": "2020-12-28T15:31:18.653305", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "Waiting for application shutdown."}
{"timestamp": "2020-12-28T15:31:18.653449", "level": "INFO", "service": "Helloworld", "instance": "84cc35a9-965e-4ac9-9f45-6554341c0dc2", "type": "internal", "message": "LifespanCycleState.SHUTDOWN:  'lifespan.shutdown.complete' event received from application."}
END RequestId: b7cd3c8d-6c70-4194-b5bd-6a0b8e766b1f
REPORT RequestId: b7cd3c8d-6c70-4194-b5bd-6a0b8e766b1f  Init Duration: 0.42 ms  Duration: 308.38 ms     Billed Duration: 400 ms Memory Size: 3008 MB    Max Memory Used: 3008 MB
```

And the lambda output :

```json
{"isBase64Encoded": false, "statusCode": 200, "headers": {"content-length": "25", "content-type": "application/json", "x-correlation-id": "e6ccda71-c841-40de-8208-aff40a2b155b"}, "body": "{\"message\":\"Hello World\"}"}
```

### Deploy the application on AWS

[Step by step guide to deploy the application on AWS using console](./documentation/deployment/awsconsole/aws_console.md)
