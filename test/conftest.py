import os
import pytest
import boto3
from moto import mock_s3


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"
    os.environ["CSV_IMPORT_BUCKET"] = "script.hive"


@pytest.fixture
def s3_resource(aws_credentials):
    with mock_s3():
        yield boto3.resource('s3', region_name="ap-southeast-2")
