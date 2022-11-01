import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Owner(Base):
    __tablename__ = "owner"
    owner_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String)
    name = sq.Column(sq.String)


class User(Base):
    __tablename__ = "user"
    user_id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    name = sq.Column(sq.String(length=60))
    last_name = sq.Column(sq.String(length=60))
    link_profile = sq.Column(sq.String)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey("owner.owner_id"))
    owner = relationship("Owner", backref='user')
    is_favorites = sq.Column(sq.Boolean)
    is_in_black_list = sq.Column(sq.Boolean)

    # def __str__(self):
    #     return f"{self.vk_id}"


class Photo(Base):
    __tablename__ = "photo"
    photo_id = sq.Column(sq.Integer, primary_key=True)
    link_photo_1 = sq.Column(sq.String)
    link_photo_2 = sq.Column(sq.String)
    link_photo_3 = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", backref="photo")


def create_table(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
