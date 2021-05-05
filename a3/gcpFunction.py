from google.cloud import storage
from google.cloud import logging
from datetime import datetime
import cloudstorage as gcs


def hello_gcs(event, context):
    # creating connection to buckets
    storage_client = storage.Client()

    # getting information to create backup
    file = event
    bucketName = 'kbigelow-test'
    fileName = format(file['name'])
    bucketName2 = 'copytwokayleebigelow'

    try:
        # creating connection to buckets
        source_bucket = storage_client.bucket(bucketName)
        dest_bucket = storage_client.bucket(bucketName2)

        # copying file to backup bucket
        blob = source_bucket.blob(fileName)
        blob_copy = source_bucket.copy_blob(blob, dest_bucket)

        print(f"Making backup of file: {file['name']}.")

        # getting time for logs
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # getting current log file
        try:
            blob3 = dest_bucket.get_blob("log.txt")
            contents = blob3.download_as_string().decode('utf-8')
        except Exception as e:
            contents = 'Logs of Backup Function\n\n'

        # appending to log file
        newLog = '\nMade backup of ' + str(fileName) + '\nTime: ' + str(
            dt_string) + '\nSource Bucket: ' + bucketName + '\nBackup Bucket: ' + bucketName2 + '\n\n'
        new_contents = str(contents) + str(newLog)

        # uploading log file
        blob2 = dest_bucket.blob("log.txt")
        blob2.upload_from_string(new_contents)

        print("Created backup")
    except Exception as e:
        print(e)
        print('Error creating backup of file {} from bucket {}.'.format(
            fileName, bucketName))
