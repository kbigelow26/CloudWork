#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: October 3, 2020
This program creates a table called encodings on aws with boto3
"""

import boto3
import csv


def generateTable():
    """
    This function generates a table in aws dynamoDB
    req: encodings.csv to be on the same level as this file
        ~/.aws/credentials to be set up with aws credentials
    """
    resource = boto3.resource('dynamodb', 'us-east-1')
    try:
        # create table called encodings
        params = {
            'TableName': 'encodings',
            'KeySchema': [
                {'AttributeName': 'col', 'KeyType': 'HASH'},
                {'AttributeName': 'short', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'short', 'AttributeType': 'S'},
                {'AttributeName': 'col', 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }
        table = resource.create_table(**params)
        print("Table is creating...")
        # waits for table to be created so no errors occur in load
        table.wait_until_exists()
        print("Table has been created")
        # reads in the csv file
        print("Adding information to table...")
        with open('encodings.csv') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            # adds each row of the csv to the table
            for row in read:
                table.put_item(
                    Item={
                        'short': row[0],
                        'expanded': row[1],
                        'col': row[2]
                    }
                )
        print("Information has been added to table")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    generateTable()
