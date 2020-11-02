Name: Kaylee Bigelow
Date: Novemeber 03, 2020
Course: CIS*4010

Assignment 2

General:
    Python Modules:
        - boto3
        - csv
        - paramiko
        - time
        - scp
        - os

Part 1:
launch.py
    Preconditions:
        1) User creates deployment description files (also refered to as config files)
            No feild may be blank unless specified below
            - template.csv with information:
                - Template Name
                - Amazon Machine Image (ami)
                - Instance Type
                - Root Volume Size (GiB)
                - Security Group Name
                - Region
            - instances.csv with information:
                - Template Name
                - Instance Name
                - ssh key Name
                - Container Package Name
            - container.csv with information:
                - Container Package Name
                - Container
                - Location
                - Start script (may be left blank)
        2) If a start script is referanced in container.csv it must exist in the same 
            directory as launch.py
        3) The user must create ssh keys in the aws console and save the private key in 
            the same directory as launch.py
        4) The docker containers must exist in the specified locations
        5) The user must have their aws credentials saved in .aws/credentials on their system
    How to Run:
        >
    Bonus:
        - in the container.csv file the user can specify 'Local system' 
            in which case the program will find the docker image on the
            local system and put that onto the instance
    Error conditions:
        - "Unable to load in config files": returned if unable to find or 
            parse congif files
        - If an error occurs while creating instances the error will be printed to the user

monitor.py
    How to Run:
        >
    Information displayed:
        - Instance Name
        - Instance State
        - Instance Id
        - Availability Zone
        - Image Id
        - Instance Type
        - Volume Size
        - SSH Key Name
        - Public Ip
        - Security Groups
        - Root Device Name
        - System
        - Docker Containers Running