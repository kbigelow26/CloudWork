#!usr/bin/python3

import boto3
import csv


def generateTable(file, tableName):
    resource = boto3.resource('dynamodb', 'us-east-1')
    # read in file
    try:
        # create table
        params = {
            'TableName': tableName,
            'KeySchema': [
                {'AttributeName': 'commodity#variable', 'KeyType': 'HASH'},
                {'AttributeName': 'year', 'KeyType': 'RANGE'},
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'commodity#variable', 'AttributeType': 'S'},
                {'AttributeName': 'year', 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }

        table = resource.create_table(**params)
        print("Table is creating...")
        table.wait_until_exists()
        print("Table has been created")
        # put stuff in table
        with open(file) as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                # print(row[0])
                table.put_item(
                    Item={
                        'commodity#variable': row[0]+"#"+row[1],
                        'commodity': row[0],
                        'variable': row[1],
                        'year': row[2],
                        'units': row[3],
                        'mfactor': row[4],
                        'value': row[5]
                    }
                )
        print("Information has been added to table")
    except Exception as e:
        print(e)


def main():
    print("To exit program enter 'exit'")

    while(True):
        print("Please enter CSV file name and table name:")
        userInput = input().split(" ")
        if userInput[0] == "exit":
            print("BYE!")
            exit(1)
        elif len(userInput) == 2:
            generateTable(userInput[0], userInput[1])
        else:
            print("Invalid input.\nExample input: file1.csv testTable")


if __name__ == "__main__":
    main()