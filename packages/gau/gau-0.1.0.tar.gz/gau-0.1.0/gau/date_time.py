from calendar import monthrange
from datetime import datetime, timedelta

def prev_month(dt: datetime = None) -> datetime:
    """
    Return the same day in previous month based on the given datetime.
    
    Args:
        dt (datetime, optional): The datetime to calculate the previous month from. 
            Defaults to the current datetime.
    
    Returns:
        datetime: The datetime representing the previous month.
    """
    if dt is None:
        dt = datetime.now()
    month_prev = (dt.replace(day=1) - timedelta(days=1))
    if dt.day > monthrange(month_prev.year, month_prev.month)[1]:
        return month_prev.replace(day=monthrange(month_prev.year, month_prev.month)[1])
    return month_prev.replace(day=dt.day)

