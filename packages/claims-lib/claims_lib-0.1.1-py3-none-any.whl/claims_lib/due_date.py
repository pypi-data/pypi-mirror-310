from datetime import datetime, timedelta

"""
    Calculate a due date.
    
    Args:
        days_from_now (int): The number of days from today for the due date.
    
    Returns:
        str: Due date as a simple date string in YYYY-MM-DD format.
"""

def calculate_due_date(days_from_now):
    
    due_date = datetime.now() + timedelta(days=days_from_now)
    return due_date.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
