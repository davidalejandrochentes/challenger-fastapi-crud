import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base
from models.mixins.db_mixin import SoftDeleteMixin, TimestampMixin

class Review(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'reviews'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    rating = sa.Column(sa.Integer)
    comment = sa.Column(sa.Text)
    recipe_id = sa.Column(sa.Integer, sa.ForeignKey('recipes.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    recipe = relationship("Recipe", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
