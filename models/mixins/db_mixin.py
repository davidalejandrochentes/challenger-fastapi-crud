import sqlalchemy as sa
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime, nullable=True)
