-- Import csv data to DynamoDB table
INSERT OVERWRITE TABLE dynamodb_contacts
  SELECT DISTINCT id, CONCAT_WS(' ',first_name,last_name),email,
                  gender, address, language FROM csv_contacts
  WHERE
    created_date >= '${TODAY}'
