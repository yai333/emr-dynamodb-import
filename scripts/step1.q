-- Create external table for dynamodb table.
CREATE EXTERNAL TABLE IF NOT EXISTS
  dynamodb_contacts (
    id string,full_name string, email string,
    gender string,address string,language array<string>)
  STORED BY
    'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
  TBLPROPERTIES
    ("dynamodb.table.name" = "${DYNAMODBTABLE}",
     "dynamodb.column.mapping" = "id:id,full_name:full_name,email:email,gender:gender,address:address,language:language");
