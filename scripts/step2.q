-- Create table using csv in s3
CREATE EXTERNAL TABLE IF NOT EXISTS
  csv_contacts (id string,first_name string,
                last_name string, email string, gender string,
                address string, language array<string> )
  PARTITIONED BY (created_date string)
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
  COLLECTION ITEMS TERMINATED BY ','
  LOCATION '${INPUT}/uploads/'
  TBLPROPERTIES (
    'serialization.null.format' = '',
    'skip.header.line.count' = '1');
