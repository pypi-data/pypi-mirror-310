from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key

'''
    Function to count number of maintenance records due in specified period
    Parameters are 
        user_id = user id of the logged in user
        start_date = start_date of the range
        end_date = end_date of the range
        table_name = DynamoDB table name
    return: calculated upcoming maintenance records for user (int)
'''

def count_upcoming_maintenance(user_id, days, table_name):
    #calculate the start and end dates based on today's date
    today = datetime.today()
    start_date = today.strftime('%Y-%m-%d')  # 'YYYY-MM-DD' format
    end_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')  # calculate the end date

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(
            FilterExpression=(
                Key('user_id').eq(user_id) & 
                Key('next_service_date').between(start_date, end_date)
            )
        )
        return response.get("Count", 0)
    except Exception as e:
        print(f"Error counting upcoming maintenance records for user: {e}")
        return 0