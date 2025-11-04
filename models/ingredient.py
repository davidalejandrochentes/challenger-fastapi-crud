import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin, TimestampMixin

class Ingredient(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'ingredients'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, index=True)
    category = sa.Column(sa.String)

    recipes = relationship("RecipeIngredient", back_populates="ingredient")
