from datetime import datetime
from dateutil.relativedelta import relativedelta

"""
    Function to calculate the next service date based on the last service date and service interval
    Parameters:
        last_service_date: Date of the last service
        service_interval_months: Number of months until the next service is due
    return: calculated next service date in 'YYYY-MM-DD' format (string)
"""

def calculate_next_service_date(last_service_date, service_interval_months):
    
    last_service = datetime.strptime(last_service_date, "%Y-%m-%d")
    next_service_due = last_service + relativedelta(months=service_interval_months)
    return next_service_due.strftime("%Y-%m-%d")
