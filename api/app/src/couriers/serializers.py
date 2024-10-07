import re
from rest_framework import serializers
from src.couriers.services.couriers_service import get_worker_by_id
from src.couriers.services.couriers_core import InputDataType, WorkerCategory, WorkerStatus


def is_phone_valid(phone: str):
    validate_phone_pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
    is_valid = bool(re.match(validate_phone_pattern, phone))
    return True if is_valid else False


def validate_worker_id(worker_id):
    worker = get_worker_by_id(worker_id)
    if not worker:
        return worker
    else:
        raise serializers.ValidationError("Worker with such id doesn't exist")


def validate_couriers_category(category):
    is_category_valid = category in [cat.value for cat in WorkerCategory]
    if is_category_valid:
        return category
    else:
        raise serializers.ValidationError("Invalid worker category")


def validate_couriers_status(status):
    is_status_valid = str(status) in [st.value for st in WorkerStatus]
    if is_status_valid:
        return status
    else:
        raise serializers.ValidationError("Invalid worker status")


class BaseSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField(allow_null=True, default=None)
    phone = serializers.ListField(child=serializers.CharField())

    def validate_phone(self, value):
        valid_phones = list()
        for phone in value:
            if is_phone_valid(phone):
                valid_phones.append(phone)
        if len(valid_phones) > 0:
            return valid_phones
        else:
            raise serializers.ValidationError("No valid phone numbers received")


class Service1Serializer(BaseSerializer):
    id = serializers.UUIDField(required=False)
    status = serializers.IntegerField()
    category = serializers.CharField()
    document = serializers.CharField(allow_null=True, default=None)

    def validate(self, data):
        try:
            if "id" in data:
                validate_worker_id(data["id"])
            validate_couriers_status(data["status"])
            validate_couriers_category(data["category"])
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class Service2Serializer(BaseSerializer):
    id = serializers.UUIDField(required=False)
    status = serializers.IntegerField()

    def validate(self, data):
        try:
            if "id" in data:
                validate_worker_id(data["id"])
            validate_couriers_status(data["status"])
            return data
        except Exception as e:
            raise serializers.ValidationError(e)


class Service3Serializer(BaseSerializer):
    document = serializers.CharField(allow_null=True, default=None)


class Service4Serializer(BaseSerializer):
    pass


def get_serializer(data_type: InputDataType, request_data):
    if data_type == InputDataType.SERVICE1:
        return Service1Serializer(data=request_data)
    elif data_type == InputDataType.SERVICE2:
        return Service2Serializer(data=request_data)
    elif data_type == InputDataType.SERVICE3:
        return Service3Serializer(data=request_data)
    elif data_type == InputDataType.SERVICE4:
        return Service4Serializer(data=request_data)
    else:
        return None
