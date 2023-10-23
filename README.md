# recog-code-challenge Super Smart Medical Assistant Lambda

## Description

This is a code challenge for Recog. The challenge is to create a simple endpoint that allows a user to enter a list of symptoms and receive a possible diagnosis.

## Run tests

1. Install tox globally: `pip install tox`
2. Run tox: `tox`

Code coverage is generated in the `htmlcov` directory.

## Run locally

You will need setup openai api key `env.json` file. You can use `env.json.example` as a template.

1. Install dependencies: `pip install -r requirements.txt`
2. Run SAM build: `sam build`
3. Run SAM local: `sam local start-api --env-vars env.json`

## Invoke locally

1. Install dependencies: `pip install -r requirements.txt`
2. Run SAM build: `sam build`
3. Run SAM local: `sam local invoke SmartMedicalAssistantFunction  --event events/diagnosis.json --env-vars env.json`

## Deploy

First need to create ssm parameter with openai api key:

```bash
aws ssm put-parameter --name /recog/OPENAI_API_KEY:1' --value <api_key> --type SecureString
```

Then run:

```bash
sam deploy --guided
```
