import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Example(SqlAlchemyBase):
    __tablename__ = 'examples'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    example = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    example_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hardness = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    right = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)

    user = orm.relationship('User')

    def __repr__(self):
        return f'<Example> {self.id} {self.user_id} {self.example}'
