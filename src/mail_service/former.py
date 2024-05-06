from datetime import datetime
from enum import Enum


class TimeType(Enum):
    START = "start"
    END = "end"


def form_string(type: TimeType) -> str:
    if type == TimeType.START:
        return "Your booking starts over 15 minutes."
    elif type == TimeType.END:
        return "Your booking ends over 15 minutes."
