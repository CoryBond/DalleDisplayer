from datetime import datetime
from typing import List


def get_current_sortable_datetime_strs() -> List[str]:
    now = datetime.now()
    return [now.date().isoformat(), now.time().isoformat()]