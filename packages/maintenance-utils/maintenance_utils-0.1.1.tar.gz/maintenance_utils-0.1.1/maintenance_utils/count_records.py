import boto3
from boto3.dynamodb.conditions import Key
'''
    Function to counts number of records in given DynamoDB table
    Parameters:
        table_name: name of the DynamoDB table
        user_id: user ID to filter the records.
    return: calculated total records in the table for user (int)
'''

def count_records(table_name, user_id):
   
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    
    try:
        response = table.scan(
            FilterExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id}
        )
        return response.get("Count", 0)
    except Exception as e:
        print(f"Error counting records in DynamoDB table: {e}")
        return 0