import datetime
from typing import Any

def _check_expiration_date(valid_until: datetime) -> bool:
    if valid_until < datetime.date.today():
        return False
    return True
