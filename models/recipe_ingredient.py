import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    recipe_id = sa.Column(sa.Integer, sa.ForeignKey('recipes.id'))
    ingredient_id = sa.Column(sa.Integer, sa.ForeignKey('ingredients.id'))
    quantity = sa.Column(sa.String)
    unit = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")
