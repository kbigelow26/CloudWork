#!usr/bin/python3

import boto3
import csv
from boto3.dynamodb.conditions import Key, Attr


def queryTable(commodity):
    resource = boto3.resource('dynamodb', 'us-east-1')
    try:
        encodingTable = resource.Table("encodings")
        response = encodingTable.query(
            KeyConditionExpression=Key('col').eq('commodity'))
        validComm = False
        for comm in response['Items']:
            if comm['short'] == commodity:
                validComm = True
            elif comm['expanded'] == commodity:
                commodity = comm['short']
                validComm = True
        if validComm == False:
            print("Invalid commodity")
            return
        response = encodingTable.query(
            KeyConditionExpression=Key('col').eq('variable'))
        variables = response['Items']
        tableNA = resource.Table("northamerica")
        tableCAN = resource.Table("canada")
        tableUSA = resource.Table("usa")
        tableMEX = resource.Table("mexico")
        OverallCANUSATally = 0
        OverallCANUSAMEXTally = 0
        OverallNeitherTally = 0
        for var in variables:
            responseNA = tableNA.query(KeyConditionExpression=Key('commodity').eq(
                commodity) & Key('variable#year').begins_with(var['short']))
            if responseNA['Items']:
                # add to table
                NAInfo = []
                YearInfo = []
                for curr in responseNA['Items']:
                    NAInfo.append(round(float(curr['value']), 3))
                    YearInfo.append(curr['year'])

                CANInfo = []
                responseCAN = tableCAN.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                # add to table
                for curr in responseCAN['Items']:
                    CANInfo.append(round(float(curr['value']), 3))

                USAInfo = []
                responseUSA = tableUSA.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                # add to table
                for curr in responseUSA['Items']:
                    USAInfo.append(round(float(curr['value']), 3))

                MEXInfo = []
                responseMEX = tableMEX.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                # add to table
                for curr in responseMEX['Items']:
                    MEXInfo.append(round(float(curr['value']), 3))

                # do calc
                CANUSAInfo = []
                CANUSAMEXInfo = []
                DefInfo = []
                CANUSATally = 0
                CANUSAMEXTally = 0
                NeitherTally = 0
                for curr in range(len(CANInfo)):
                    CANUSAInfo.append(
                        round(CANInfo[curr]+USAInfo[curr], 3))
                    CANUSAMEXInfo.append(
                        round(CANInfo[curr]+USAInfo[curr]+MEXInfo[curr], 3))
                    if CANUSAInfo[curr] == NAInfo[curr]:
                        DefInfo.append("CAN+USA")
                        CANUSATally = CANUSATally + 1
                        OverallCANUSATally = OverallCANUSATally + 1
                    elif CANUSAMEXInfo[curr] == NAInfo[curr]:
                        DefInfo.append("CAN+USA+MEX")
                        CANUSAMEXTally = CANUSAMEXTally + 1
                        OverallCANUSAMEXTally = OverallCANUSAMEXTally + 1
                    else:
                        DefInfo.append("Neither")
                        NeitherTally = NeitherTally + 1
                        OverallNeitherTally = OverallNeitherTally + 1
                # print
                print("Commodity: "+commodity)
                print("Variable: "+var['expanded'])
                print("{:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}".format(
                    "Year", "North America", "Canada", "USA", "Mexico", "CAN+USA", "CAN+USA+MEX", "NA Defn"))
                # print(
                #     "Year\t\tNorth America\t\tCanada\t\tUSA\t\tMexico\t\tCAN+USA\t\tCAN+USA+MEX\t\tNA Defn")
                for curr in range(len(YearInfo)):
                    print("{:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}".format(YearInfo[curr], str(NAInfo[curr]), str(
                        CANInfo[curr]), str(USAInfo[curr]), str(MEXInfo[curr]), str(CANUSAInfo[curr]), str(CANUSAMEXInfo[curr]), DefInfo[curr]))
                    # print(YearInfo[curr]+"\t\t"+str(NAInfo[curr])+"\t\t" +
                    #       str(CANInfo[curr])+"\t\t"+str(USAInfo[curr])+"\t\t"+str(MEXInfo[curr])+"\t\t"+str(CANUSAInfo[curr])+"\t\t"+str(CANUSAMEXInfo[curr])+"\t\t"+DefInfo[curr])
                print("North America Definition Results: " + str(CANUSATally) +
                      " CAN+USA, "+str(CANUSAMEXTally)+" CAN+USA+MEX, "+str(NeitherTally)+" Neither")
                if CANUSATally > CANUSAMEXTally and CANUSATally > NeitherTally:
                    print("Therefore we conclude North America = CAN+USA")
                elif CANUSAMEXTally > CANUSATally and CANUSAMEXTally > NeitherTally:
                    print("Therefore we conclude North America = CAN+USA+MEX")
                elif NeitherTally > CANUSATally and NeitherTally > CANUSAMEXTally:
                    print("Therefore we conclude North America = Neither")
                else:
                    print(
                        "Therefore we can not conclude the definition of North America\n")

        print("Overall North America Definition Results: " + str(OverallCANUSATally) +
              " CAN+USA, "+str(OverallCANUSAMEXTally)+" CAN+USA+MEX, "+str(OverallNeitherTally)+" Neither")
        if OverallCANUSATally > OverallCANUSAMEXTally and OverallCANUSATally > OverallNeitherTally:
            print("Therefore we conclude North America = CAN+USA")
        elif OverallCANUSAMEXTally > OverallCANUSATally and OverallCANUSAMEXTally > OverallNeitherTally:
            print("Therefore we conclude North America = CAN+USA+MEX")
        elif OverallNeitherTally > OverallCANUSATally and OverallNeitherTally > OverallCANUSAMEXTally:
            print("Therefore we conclude North America = Neither")
        else:
            print("Therefore we can not conclude the definition of North America\n")
    except Exception as e:
        print(e)


def main():
    print("To exit program enter 'exit'")

    while(True):
        print("Please enter the commodity or code for the commodity:")
        userInput = input().split(" ")
        if userInput[0] == "exit":
            print("BYE!")
            exit(1)
        elif len(userInput) == 1:
            queryTable(userInput[0])
        else:
            print("Invalid input.\nExample input: WT\nOr enter 'exit' to exit")


if __name__ == "__main__":
    main()
