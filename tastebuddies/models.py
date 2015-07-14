from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from sqlalchemy_imageattach.entity import (
    Image,
    image_attachment
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


usertaste_table = Table('user_profile', Base.metadata,
                        Column('users', Integer, ForeignKey('users.id')),
                        Column('profile', Integer, ForeignKey('profile.id'))
                        )


userdiet_table = Table('user_diet', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('diet.id'))
                       )


usercost_table = Table('user_cost', Base.metadata,
                       Column('users', Integer, ForeignKey('users.id')),
                       Column('profile', Integer, ForeignKey('cost.id'))
                       )


groupdiscussion_table = Table('group_discussion', Base.metadata,
                              Column('group', Integer, ForeignKey('group.id')),
                              Column('discussion', Integer, ForeignKey(
                                     'discussion.id'))
                              )

groupage_table = Table('group_age', Base.metadata, Column('group', Integer,
                       ForeignKey('group.id')), Column('agegroup', Integer,
                       ForeignKey('agegroup.id'))
                       )

groupuser_table = Table('group_user', Base.metadata, Column('group', Integer,
                        ForeignKey('group.id')), Column('users', Integer,
                        ForeignKey('users.id'))
                        )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    confirmed = Column(Boolean)
    firstname = Column(Text)
    lastname = Column(Text)
    password = Column(Text, nullable=False)
    email = Column(Text)
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    food_profile = relationship('profile', secondary=usertaste_table)
    diet_restrict = relationship('diet', secondary=userdiet_table)
    cost_restrict = relationship('cost', secondary=usercost_table)
    restaurants = Column(Text)
    picture = image_attachment('UserPicture')


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    taste = Column(Text)


class AgeGroup(Base):
    __tablename__ = 'agegroup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    age_group = Column(Text)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(Text)


class Cost(Base):
    __tablename__ = 'cost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cost = Column(Text)


class Diet(Base):
    __tablename__ = 'diet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diet = Column(Text)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    picture = image_attachment('UserPicture')
    discussion = relationship('discussion', secondary=groupdiscussion_table)
    group_admin = relationship("group admin", uselist=False, backref="admin")


class Discussion(Base):
    __tablename__ = 'discussion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discussion_title = Column(Text)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discussionpost = Column(Integer, ForeignKey('discussion.id'))


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
