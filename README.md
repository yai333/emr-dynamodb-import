# Importing DynamoDB Data Using Apache Hive on Amazon EMR

## What this example accomplishes?

Every day an external datasource exports csv to S3 bucket and then load csv data to a AWS DynamoDB table.

## Prerequisites

- Setup an AWS account
- Install Serverless Framework

## Deploying Serverless Project

```
$sls deploy --stage dev --region YOUR_REGION
```

## Importing csv to DynamoDB

Upload csv file to S3 bucket

```
$aws s3 cp csv/contacts.csv s3://myemr.csv.import.dev/uploads/created_date=2020-02-03/contacts.csv
```

Then there will be a EMR cluster started automatically, that's all about it, no more step required.
