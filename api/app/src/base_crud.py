from abc import ABC
from contextlib import contextmanager
from typing import cast, Any

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session


class BaseCRUD(ABC):

    def __init__(self, db_session):
        if isinstance(db_session, sessionmaker):
            self.session: Session = cast(Session, db_session())
        else:
            self.session = db_session

    @contextmanager
    def transaction(self):
        with self.session as transaction:
            yield transaction

    def insert(self, model, **kwargs: Any):
        add_model = model(**kwargs)
        self.session.add(add_model)
        return add_model

    def commit(self):
        self.session.commit()

    def get_one_by_statement(self, stmt):
        result = self.session.execute(stmt)
        return result.unique().scalar_one()

    def update_by_statement(self, model, init_stmt):
        stmt = select(model).from_statement(init_stmt) \
            .execution_options(synchronize_session="fetch")
        result = self.session.execute(stmt)
        self.session.commit()
        return result.unique()

    def delete_by_statement(self, stmt):
        self.session.execute(stmt)
        self.session.commit()
