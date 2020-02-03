import boto3
import logging
import os
from datetime import datetime
from pathlib import Path

emr = boto3.client('emr')
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def startEMRJob(event, context):
    try:
        put_dump_record_to_db()
        put_step_scripts_to_s3()
        cluster_id = emr.run_job_flow(
            Name='test_emr_job',
            LogUri="s3://{}".format(os.environ['EMR_LOGS_BUCKET']),
            ReleaseLabel='emr-5.18.0',
            Applications=[
                {
                    'Name': 'Hadoop'
                },
                {
                    'Name': 'Livy'
                },
                {
                    'Name': 'Pig'
                },
                {
                    'Name': 'Hue'
                },
                {
                    'Name': 'Hue'
                },
                {
                    'Name': 'Hive'
                },
            ],
            Instances={
                'InstanceGroups': [
                    {
                        'Name': "Master nodes",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'MASTER',
                        'InstanceType': 'm1.medium',
                        'InstanceCount': 1,
                    },
                    {
                        'Name': "Slave nodes",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'CORE',
                        'InstanceType': 'm1.medium',
                        'InstanceCount': 2,
                    }
                ],
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                'Ec2SubnetId': os.environ['SUBNET_ID'],
            },
            Configurations=[
                {
                    'Classification': 'hive-site',
                    'Properties': {
                        'hive.execution.engine': 'mr'
                    }
                },
            ],
            Steps=[
                {
                    'Name': 'creating dynamodb table',
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': ['hive-script',
                                     '--run-hive-script',
                                     '--args',
                                     '-f',
                                     's3://{}/scripts/step1.q'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'DYNAMODBTABLE={}'.format(
                                         os.environ["CONTACTS_TABLE"])]
                    }
                },
                {
                    'Name': 'creating csv table',
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': ['hive-script',
                                     '--run-hive-script',
                                     '--args',
                                     '-f',
                                     's3://{}/scripts/step2.q'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'INPUT=s3://{}'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'TODAY={}'.format(
                                         datetime.today().strftime('%Y-%m-%d'))]
                    }
                },
                {
                    'Name': 'adding partition',
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': ['hive-script',
                                     '--run-hive-script',
                                     '--args',
                                     '-f',
                                     's3://{}/scripts/step3.q'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'INPUT=s3://{}'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'TODAY={}'.format(
                                         datetime.today().strftime('%Y-%m-%d'))]
                    }
                },
                {
                    'Name': 'import date to dynamodb',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': ['hive-script',
                                     '--run-hive-script',
                                     '--args',
                                     '-f',
                                     's3://{}/scripts/step4.q'.format(
                                         os.environ['CSV_IMPORT_BUCKET']),
                                     '-d',
                                     'TODAY={}'.format(
                                         datetime.today().strftime('%Y-%m-%d'))]
                    }
                }
            ],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole',
        )
        logger.info('cluster {} created with the step...'.format(
            cluster_id['JobFlowId']))

    except Exception as e:
        logger.error(e)
        raise


def put_dump_record_to_db():
    table = dynamodb.Table(os.environ["CONTACTS_TABLE"])
    if table.item_count == 0:
        table.put_item(
            Item={'id': 'NA',
                  'full_name': 'demo user',
                  'gender': 'M',
                  'address': 'NA',
                  'language': ["English"]})


def put_step_scripts_to_s3():
    root_path = Path(__file__).parent.parent
    scripts = ["scripts/step1.q",
               "scripts/step2.q",
               "scripts/step3.q",
               "scripts/step4.q"]
    for script in scripts:
        s3.Bucket(os.environ['CSV_IMPORT_BUCKET']).upload_file(
            '{}/{}'.format(root_path, script), script)
