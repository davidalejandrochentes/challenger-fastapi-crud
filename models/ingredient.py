import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin

class Ingredient(Base, SoftDeleteMixin):
    __tablename__ = 'ingredients'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, index=True)
    category = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    recipes = relationship("RecipeIngredient", back_populates="ingredient")
