import enum
from dataclasses import dataclass
from typing import Optional


class InputDataType(str, enum.Enum):
    SERVICE1 = 1
    SERVICE2 = 2
    SERVICE3 = 3
    SERVICE4 = 4


class WorkerCategory(str, enum.Enum):
    DRIVER = "driver"
    COURIER = "courier"


class WorkerStatus(str, enum.Enum):
    FIRED = 1
    TEMPORARILY_NOT_WORKING = 2
    WORKING = 3


@dataclass
class CouriersData:
    first_name: str
    last_name: str
    status: WorkerStatus
    category: WorkerCategory
    patronymic: Optional[str] = None
    document: Optional[str] = None
