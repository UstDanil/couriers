import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from src.couriers.serializers import get_serializer
from src.couriers.services.couriers_service import SavingService
from src.couriers.services.couriers_core import InputDataType

logger = logging.getLogger('app')


class CouriersController(viewsets.ViewSet):
    serializer_classes = {
        "create": None
    }

    def create(self, request, num):
        try:
            is_num_valid = str(num) in [el.value for el in InputDataType]
            if not is_num_valid:
                logger.error('Unknown service number')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data_type = InputDataType(str(num))

            serializer = get_serializer(data_type, request.data)
            if not serializer:
                logger.error('There is no serializer specified for this service type.')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.is_valid(raise_exception=True)

            worker_id = SavingService(data_type, serializer.data).save_data()
            if worker_id:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e, exc_info=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)

