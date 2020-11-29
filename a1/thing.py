from google.cloud import storage


def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    storage_client = storage.Client()

    file = event
    bucketName = 'kbigelow-test'
    fileName = format(file['name'])
    bucketName2 = 'copytwokayleebigelow'

    source_bucket = storage_client.bucket(bucketName)
    source_blob = storage_client.blob(fileName)
    dest_bucket = storage_client.bucket(bucketName2)

    blob_copy = source_bucket.copy_blob(source_blob, dest_bucket, 'logs.txt')

    print(f"Processing file: {file['name']}.")

    gcs_file = gcs.open(filename, 'w', content_type='text/plain', options={
                        'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'}, retry_params=write_retry_params)
  gcs_file.write('abcde\n')
  gcs_file.write('f'*1024*4 + '\n')
