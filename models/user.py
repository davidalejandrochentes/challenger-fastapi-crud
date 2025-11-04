import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin, TimestampMixin

class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    password_hash = sa.Column(sa.String)
    full_name = sa.Column(sa.String)
    bio = sa.Column(sa.Text, nullable=True)

    recipes = relationship("Recipe", back_populates="user")
    reviews = relationship("Review", back_populates="user")
