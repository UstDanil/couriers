# Couriers
Сохранение в базу работников с возможностью предоставления данных из разных сервисов

## Запуск 

make run 

## Стэк технологий

- Python
- DjangoRestFramework
- Unittest
- PostgreSQL
- SQLAlchemy
- Alembic
- Poetry
- Pylint
- Docker

## Запуск тестов

docker exec -it api-couriers-api-1 bash

cd src

python manage.py test tests 
