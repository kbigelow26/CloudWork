Name: Kaylee Bigelow
Date: November 14, 2020
Course: CIS*4010

Assignment 3

Cloud System 1: AWS
  Triggers from bucket: kbigelow-test on S3
  Copies to bucket: copytwokayleebigelow on S3
  Name of file containing function code: awsFunction.py
  Programming language used: Python
  How I set ip the function: 
    - Using the AWS console I created a lambda function. I selected
      a blueprint that triggers off of a upload to a S3 bucket. Then
      I changed almost all of the code in the blueprint and used
      boto3 to copy the file, read in the log file (if it exists),
      and upload the new log file.

Could System 2: GCP
  Triggers from bucket: kbigelow-test on buckets
  Copies to bucket: copytwokayleebigelow on buckets
  Name of file containing function code: gcpFunction.py
  Programming language used: Python
  How I set ip the function: 
    - Using the GCP console I created a cloud fucntion. I selected 
      a trigger type of Cloud Storage - Finalize/Create with my 
      bucket. Then using google.cloud I copy the file, read in the
      log file (if it already exists), and then upload the log file 
      with the new log entry.

Limitation of AWS: due to the nature of S3 buckets uploading files
  asynchronously this triggers the lambda function asynchronously
  which then may cause some logs to not be written when uploading 
  more than 1 file at a time.

Preconditions: the buckets must exist with the correct names