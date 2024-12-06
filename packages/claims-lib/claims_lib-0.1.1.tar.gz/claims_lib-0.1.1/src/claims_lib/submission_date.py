from datetime import datetime

"""
Get the current submission date.

Returns:
    str: Submission date as a simple date string in YYYY-MM-DD format.
"""

def get_submission_date():
    submission_date = datetime.now()
    return submission_date.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
