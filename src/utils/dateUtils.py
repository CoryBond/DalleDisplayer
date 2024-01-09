from datetime import datetime


def get_current_sortable_datetime_strs() -> [str]:
    now = datetime.now()
    return [now.date().isoformat(), now.time().isoformat()]