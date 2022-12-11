from dataclasses import dataclass
import datetime


@dataclass
class NotificationDTO:
    id: str
    content: str
    date_and_time: datetime
