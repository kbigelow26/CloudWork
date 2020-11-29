Name: Kaylee Bigelow
Date: November 29, 2020
Course: CIS*4010

Assignment 4

IBM Cloud Function:
  File: ibmFunction.py
  Steps: 
    1) Create 2 buckets
    2) Create namespace
    3) Give namespce read and write access to the buckets
        > go to IAM console to Service Ids
        > select the namespace
        > add a new access policy
    4) Create an API key for the namespace
        > IAM console -> Service Ids -> namespace -> API Keys -> create
        > copy the key
    5) Get the service instance id of the buckets
        > go to Cloud Object Storage-lu -> service credentials
        > select either bucket
        > copy the 'resource_instance_id'
    6) Get the endpoint for the buckets
        > go to Cloud Object Storage-lu -> service credentials
        > select either bucket
        > go to the link listed under endpoints
        > copy the endpoint for your region
    7) Create a trigger
        > Type: Cloud Object Storage 
        > Configuration -> bucket: first bucket
    8) Create an action in the trigger
        > Runtime: Python 3.7
    9) Enable webaction for the action
    10) Add the parameters to the Function
        > keyAPI1 : "<key_from_step_4>"
        > bucket1CNR : "<service_instance_id_from_step_5>"
        > endpoint1 : "<endpoint_from_steo_6>"
    11) Add the code from ibmFunction.py file

GCP App Engine:
  Folder: gcpAppEngine
  Main File: main.py
  Steps:
    1) Connect to testing Project
    2) Open Cloud Shell
    3) Clone this repo
    4) cd a4/gcpAppEngine
      To Test:
        5) virtualenv --python python3 ~/envs/gcpAppEngine
        6) source ~/envs/gcpAppEngine/bin/activate
        7) pip install -r requirements.txt
        8) python main.py
        9) click the Web Preview button to see the website on port 8080
      To Deploy:
        5) gcloud app create
        6) gcloud app deploy app.yaml --project <your_project_name>
        7) see the website on https://<your_project_name>.ue.r.appspot.com/