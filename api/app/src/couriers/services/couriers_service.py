import logging

from src.couriers.services.couriers_core import InputDataType, CouriersData, WorkerCategory, WorkerStatus
from src.couriers.services.couriers_repository import WorkerRepository

logger = logging.getLogger('app')


class SavingService:
    def __init__(self, data_type: InputDataType, data):
        pass
        self.data_type = data_type
        self.data = data

    def get_object_to_save(self):
        worker_id = None
        if self.data_type in (InputDataType.SERVICE1, InputDataType.SERVICE2):
            if "id" in self.data and self.data["id"]:
                worker_id = self.data["id"]

        if self.data_type == InputDataType.SERVICE1:
            return worker_id, CouriersData(
                first_name=self.data["first_name"], last_name=self.data["last_name"],
                patronymic=self.data["patronymic"], status=WorkerStatus(str(self.data["status"])),
                category=WorkerCategory(self.data["category"]), document=self.data["document"]
            )
        elif self.data_type == InputDataType.SERVICE2:
            return worker_id, CouriersData(
                first_name=self.data["first_name"], last_name=self.data["last_name"],
                patronymic=self.data["patronymic"], status=WorkerStatus(str(self.data["status"])),
                category=WorkerCategory.DRIVER
            )
        elif self.data_type == InputDataType.SERVICE3:
            return worker_id, CouriersData(
                first_name=self.data["first_name"], last_name=self.data["last_name"],
                patronymic=self.data["patronymic"], status=WorkerStatus.WORKING,
                category=WorkerCategory.DRIVER, document=self.data["document"]
            )
        elif self.data_type == InputDataType.SERVICE4:
            return worker_id, CouriersData(
                first_name=self.data["first_name"], last_name=self.data["last_name"],
                patronymic=self.data["patronymic"], status=WorkerStatus.WORKING,
                category=WorkerCategory.COURIER
            )

    def save_data(self):
        worker_id, worker_obj = self.get_object_to_save()
        db = WorkerRepository()
        if worker_id:
            db.update_worker(worker_id, worker_obj)
        else:
            worker_id = db.create_worker(worker_obj)

        db.delete_worker_phones(worker_id)
        for phone in self.data["phone"]:
            db.create_worker_phone(worker_id, phone)

        return worker_id


def get_worker_by_id(worker_id):
    db = WorkerRepository()
    return db.get_worker_by_id(worker_id)
