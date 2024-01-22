from datetime import datetime
from typing import List


def generate_ios_date_time_strs() -> List[str]:
    """
    Gets the current date and time in ISO format. 
    Will be seperated in a tuple where date is the first index and time is the second index.
    """
    now = datetime.now()
    return [now.date().isoformat(), now.time().isoformat()]