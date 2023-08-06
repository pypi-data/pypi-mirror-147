from datetime import datetime
import uuid

from sqlalchemy import DateTime, Column, TypeDecorator, CHAR, MetaData
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})


class UUIDField(TypeDecorator):
    impl = CHAR

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('length', 32)
        super().__init__(*args, **kwargs)


class Base(object):
    id = Column(UUIDField,
                primary_key=True,
                nullable=False,
                default=lambda: uuid.uuid4().hex)


class UUIDFieldWithDash(TypeDecorator):
    impl = CHAR

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('length', 36)
        super().__init__(*args, **kwargs)


DeclarativeBase = declarative_base(cls=Base, metadata=meta)
EmptyDeclarativeBase = declarative_base(metadata=meta)


class ModificationTimeMixing:
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=True
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )
    deleted_at = Column(
        DateTime,
        nullable=True
    )


class UUIDField(TypeDecorator):
    impl = CHAR

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('length', 32)
        super().__init__(*args, **kwargs)


class UUIDFieldWithDash(TypeDecorator):
    impl = CHAR

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('length', 36)
        super().__init__(*args, **kwargs)
