from uuid import uuid4
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

from src.couriers.models import Worker, WorkerPhone

from src.base_crud import BaseCRUD
from src.init_database import Session


class WorkerRepository:
    def __init__(self):
        self.db_session = Session
        self.model = Worker
        self.model_phone = WorkerPhone
        self.base = BaseCRUD(db_session=self.db_session)

    def create_worker(self, worker):
        new_worker_id = uuid4()
        with self.base.transaction():
            self.base.insert(
                self.model,
                id=new_worker_id,
                first_name=worker.first_name,
                last_name=worker.last_name,
                patronymic=worker.patronymic,
                status=worker.status.value,
                category=worker.category.value,
                document=worker.document,
            )
            self.base.commit()
        return new_worker_id

    def create_worker_phone(self, worker_id, phone):
        with self.base.transaction():
            self.base.insert(
                self.model_phone,
                id=uuid4(),
                worker_id=worker_id,
                phone=phone,
            )
            self.base.commit()

    def update_worker(self, worker_id, worker):
        try:
            stmt = update(self.model).where(
                self.model.id == worker_id
            ).values(
                first_name=worker.first_name,
                last_name=worker.last_name,
                patronymic=worker.patronymic,
                status=worker.status.value,
                category=worker.category.value,
                document=worker.document,
            ).returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None

    def get_worker_by_id(self, worker_id):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.id == worker_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def delete_worker_phones(self, worker_id):
        try:
            stmt = delete(self.model_phone).where(self.model_phone.worker_id == worker_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None
