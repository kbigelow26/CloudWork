#!usr/bin/python3

import boto3
import csv


def generateTable():
    resource = boto3.resource('dynamodb', 'us-east-1')
    # read in file
    try:
        # create table
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
        table.wait_until_exists()
        print("Table has been created")
        # put stuff in table
        print("Adding information to table...")
        with open('encodings.csv') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                # print(row[0])
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
