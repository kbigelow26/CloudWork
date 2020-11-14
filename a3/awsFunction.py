import json
import urllib.parse
import boto3
import os

# creating boto3 connections
s3 = boto3.client('s3')
resource = boto3.resource('s3')


def lambda_handler(event, context):
    # getting information about file
    bucket = event['Records'][0]['s3']['bucket']['name']
    bucket2 = 'copytwokayleebigelow'
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        # copying the file
        response = resource.Object(bucket2, key).copy_from(
            CopySource=bucket+"/"+key)

        # creating logs in cloudwatch
        print('## ENVIRONMENT VARIABLES')
        print(os.environ)
        print('## EVENT')
        print(event)
        print('File: ' + str(key))
        print('Time: ' + str(event['Records'][0]['eventTime']))
        print('Source bucket: ' + str(bucket))
        print('Backup bucket: ' + str(bucket2))

        # gets current log file
        try:
            response2 = s3.get_object(Bucket=bucket2, Key='log.txt')
            currFile = response2['Body'].read().decode('utf-8')
        except Exception as e:
            currFile = 'Logs of Backup Function\n\n'

        # adds new log to log file
        newFile = currFile + '## ENVIRONMENT VARIABLES\n' + str(os.environ) + '\n## EVENT\n' + str(event) + '\nFile: ' + str(
            key) + '\nTime: ' + str(event['Records'][0]['eventTime']) + '\nSource bucket: ' + str(bucket) + '\nBackup bucket: ' + str(bucket2) + '\n\n'
        encoded_newFile = newFile.encode('utf-8')

        # uploading new log file
        resource.Bucket(bucket2).put_object(
            Key='log.txt', Body=encoded_newFile)
        return 'Created backup'
    except Exception as e:
        print(e)
        print('Error creating backup of file {} from bucket {}.'.format(key, bucket))
        raise e
