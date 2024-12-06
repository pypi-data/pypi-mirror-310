from datetime import datetime, timedelta, timezone

"""
    Function to count the number of claims that are due in the next specified number of days.
    
    Args:
        claims (list): A list of dictionaries, each containing a claim with a 'DueDate' field in 'YYYY-MM-DD' format.
        days (int): The number of days from today to check for due claims.
    
    Returns:
        int: The count of claims that are due in the next specified number of days.
"""

def count_claims_due_in_next_days(claims, days):
    
    # Get the current date and calculate the date 'days' from now, using UTC time
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight UTC
    end_date = today + timedelta(days=days)
    
    count = 0
    for claim in claims:
        due_date_str = claim.get('due_date')
        if due_date_str:
            
            # Check if the date string has a time part (e.g., ISO 8601 format with 'T' or 'Z')
            try:
                # Attempt to parse the date. If it's in ISO 8601 format (with time), it will be parsed correctly.
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))  # Convert 'Z' to UTC offset
            except ValueError:
                # If not in ISO 8601 format, fall back to just 'YYYY-MM-DD'
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc, hour=0, minute=0, second=0, microsecond=0)

            # Ensure both today and due_date are offset-aware
            if due_date.tzinfo is None:  # If due_date is naive, set it to UTC
                due_date = due_date.replace(tzinfo=timezone.utc)

            if today <= due_date <= end_date:
                count += 1
    return count
