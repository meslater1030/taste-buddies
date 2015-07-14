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
    validates,
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
    username = Column(Text, nullable=False, unique=True)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
<<<<<<< Updated upstream
    confirmed = Column(Boolean)
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    food_profile = relationship('Profile', secondary=usertaste_table)
    diet_restrict = relationship('Diet', secondary=userdiet_table)
    cost_restrict = relationship('Cost', secondary=usercost_table)
    user_groups = relationship('Group', secondary=groupuser_table)
=======
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    food_profile = relationship('profile', secondary=usertaste_table)
    diet_restrict = relationship('diet', secondary=userdiet_table)
    cost_restrict = relationship('cost', secondary=usercost_table)
>>>>>>> Stashed changes
    restaurants = Column(Text)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    taste = Column(Text)

    @classmethod
    def write(cls, taste=None, session=None):
        if session is None:
            session = DBSession
        instance = cls(taste=taste)
        session.add(instance)
        return instance

    def __repr__(self):
        return "<Taste(%s)>" % (self.taste)


class AgeGroup(Base):
    __tablename__ = 'agegroup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    age_group = Column(Text)

    @classmethod
    def write(cls, session=None, age_group=None):
        if session is None:
            session = DBSession
        instance = cls(age_group)
        session.add(instance)
        return instance

    def __repr__(self):
        return "<Age(%s)>" % (self.age_group)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(Text)

    @classmethod
    def write(cls, session=None, city=None):
        if session is None:
            session = DBSession
        instance = cls(city)
        session.add(instance)
        return instance

    def __repr__(self):
        return "<Location(%s)>" % (self.city)


class Cost(Base):
    __tablename__ = 'cost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cost = Column(Text)

    @classmethod
    def write(cls, session=None, cost=None):
        if session is None:
            session = DBSession
        instance = cls(cost)
        session.add(instance)
        return instance

    def __repr__(self):
        return "<Cost(%s)>" % (self.cost)


class Diet(Base):
    __tablename__ = 'diet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    diet = Column(Text)

    @classmethod
    def write(cls, session=None, diet=None):
        if session is None:
            session = DBSession
        instance = cls(diet)
        session.add(instance)
        return instance

    def __repr__(self):
        return "<Dietary Preference(%s)>" % (self.diet)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    discussion = relationship('Discussion', secondary=groupdiscussion_table)
    group_admin = relationship("Admin", uselist=False)


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
