#
# main() will be run when you invoke this action
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
# @return The output of this action, which must be a JSON object.
#
import sys
import ibm_boto3
from datetime import datetime
from ibm_botocore.client import Config, ClientError


def main(dict):
    try:
        # setup of information
        resource = ibm_boto3.resource('s3', ibm_api_key_id=dict['keyAPI1'], ibm_service_instance_id=dict['bucket1CNR'], config=Config(
            signature_version="oauth"), endpoint_url=dict['endpoint1'], region_name="us-east")
        client = ibm_boto3.client('s3', ibm_api_key_id=dict['keyAPI1'], ibm_service_instance_id=dict['bucket1CNR'], config=Config(
            signature_version="oauth"), endpoint_url=dict['endpoint1'], region_name="us-east")
        bucket = 'kbigelow-testing'
        bucket2 = 'copy-bucket'
        newFile = 'testing'
        key = dict['key']
        encoded_newFile = newFile.encode('utf-8')

        # copy file to backup bucket
        response = resource.Object(bucket2, key).copy_from(
            CopySource=bucket+"/"+key)

        # get time for the log file
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # output for built in logs
        print('File: ' + str(key))
        print('Time: ' + dt_string)
        print('Source bucket: ' + str(bucket))
        print('Backup bucket: ' + str(bucket2))

        # gets current log file
        try:
            response2 = client.get_object(Bucket=bucket2, Key='log.txt')
            currFile = response2['Body'].read().decode('utf-8')
        except Exception as e:
            currFile = 'Logs of Backup Function\n\n'

        # adds new log to log file
        newFile = currFile + 'Creating backup of file: ' + \
            str(key) + '\nTime: ' + dt_string + '\nSource bucket: ' + \
            str(bucket) + '\nBackup bucket: ' + str(bucket2) + '\n\n'
        encoded_newFile = newFile.encode('utf-8')

        # uploading new log file
        resource.Bucket(bucket2).put_object(
            Key='log.txt', Body=encoded_newFile)
        return {'message': 'Created backup'}

    except Exception as e:
        print(e)
        print('Error creating backup of file {} from bucket {}.'.format(key, bucket))
        raise e
