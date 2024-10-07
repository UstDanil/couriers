from uuid import uuid4
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects import postgresql
from src.init_database import Base

from src.couriers.services.couriers_core import WorkerCategory, WorkerStatus


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    patronymic = Column(String(), nullable=True)
    status = Column(Enum(WorkerStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    category = Column(Enum(WorkerCategory, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    document = Column(String(), nullable=True)


class WorkerPhone(Base):
    __tablename__ = 'worker_phones'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    worker_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    phone = Column(String(), nullable=False)
