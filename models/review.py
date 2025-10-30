import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    rating = sa.Column(sa.Integer)
    comment = sa.Column(sa.Text)
    recipe_id = sa.Column(sa.Integer, sa.ForeignKey('recipes.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    deleted_at = sa.Column(sa.DateTime, nullable=True)

    recipe = relationship("Recipe", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
