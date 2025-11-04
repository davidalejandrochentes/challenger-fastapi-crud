import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import TimestampMixin

class RecipeIngredient(Base, TimestampMixin):
    __tablename__ = 'recipe_ingredients'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    recipe_id = sa.Column(sa.Integer, sa.ForeignKey('recipes.id'))
    ingredient_id = sa.Column(sa.Integer, sa.ForeignKey('ingredients.id'))
    quantity = sa.Column(sa.String)
    unit = sa.Column(sa.String)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")
