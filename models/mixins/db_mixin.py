import sqlalchemy as sa
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime, nullable=True)

@declarative_mixin
class TimestampMixin:
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())