import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin

class User(Base, SoftDeleteMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    password_hash = sa.Column(sa.String)
    full_name = sa.Column(sa.String)
    bio = sa.Column(sa.Text, nullable=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    recipes = relationship("Recipe", back_populates="user")
    reviews = relationship("Review", back_populates="user")
