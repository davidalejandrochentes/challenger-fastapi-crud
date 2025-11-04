import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin, TimestampMixin

class Recipe(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'recipes'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String, index=True)
    description = sa.Column(sa.Text)
    instructions = sa.Column(sa.Text)
    prep_time = sa.Column(sa.Integer)
    cook_time = sa.Column(sa.Integer)
    servings = sa.Column(sa.Integer)
    difficulty = sa.Column(sa.Enum('easy', 'medium', 'hard', name='difficulty_enum'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    user = relationship("User", back_populates="recipes")
    reviews = relationship("Review", back_populates="recipe")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")
