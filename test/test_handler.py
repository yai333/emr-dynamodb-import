# test_handler.py
import os
from src import handler


def test_copy_step_scripts_to_s3(s3_resource):
    if s3_resource.Bucket(os.environ["CSV_IMPORT_BUCKET"]) not in s3_resource.buckets.all():
        s3_resource.create_bucket(Bucket=os.environ["CSV_IMPORT_BUCKET"],
                                  CreateBucketConfiguration={'LocationConstraint': os.environ["AWS_DEFAULT_REGION"]})
    handler.put_step_scripts_to_s3()
    obj = s3_resource.Object(
        os.environ["CSV_IMPORT_BUCKET"], "scripts/step1.q")

    script = obj.get()['Body'].read().decode('utf-8')
    assert "CREATE EXTERNAL TABLE IF NOT EXISTS" in script
