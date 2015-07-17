# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean,
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

groupage_table = Table('group_age', Base.metadata, Column('group', Integer,
                       ForeignKey('groups.id')), Column('agegroup', Integer,
                       ForeignKey('agegroup.id'))
                       )

groupuser_table = Table('group_user', Base.metadata, Column('group', Integer,
                        ForeignKey('groups.id')), Column('users', Integer,
                        ForeignKey('users.id'))
                        )

groupcost_table = Table('group_cost', Base.metadata, Column('groups_id',
                        Integer, ForeignKey('groups.id')),
                        Column('cost_id', Integer, ForeignKey('cost.id'))
                        )

grouptaste_table = Table('group_taste', Base.metadata,
                         Column('group_id', Integer, ForeignKey('groups.id')),
                         Column('profile', Integer, ForeignKey('profile.id'))
                         )


groupdiet_table = Table('group_diet', Base.metadata,
                        Column('group_id', Integer, ForeignKey('groups.id')),
                        Column('diet_id', Integer, ForeignKey('diet.id'))
                        )


class _Table(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def write(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all()

    @classmethod
    def one(cls, eid=None, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == eid).one()


class User(Base, _Table):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    confirmed = Column(Boolean, default=False)
    ver_code = Column(Integer)
    age = Column(Integer, ForeignKey('agegroup.id'))
    user_location = Column(Integer, ForeignKey('location.id'))
    cost = Column(Integer, ForeignKey('cost.id'))
    food_profile = relationship('Profile', secondary=usertaste_table,
                                backref='users')
    diet_restrict = relationship('Diet', secondary=userdiet_table,
                                 backref='users')
    user_groups = relationship('Group', secondary=groupuser_table,
                               backref='users')
    restaurants = Column(Text)
    food = Column(Text)

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    @classmethod
    def lookup_user_by_username(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(User.username == username).one()

    @classmethod
    def lookup_user_by_id(cls, uid, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == uid).one()

    @classmethod
    def addgroup(cls, session=None, usergroup=None, username=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_user_by_username(username=username)
        instance.user_groups.append(usergroup)
        session.add(instance)
        return instance

    @classmethod
    def write_ver_code(cls, username, ver_code, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_user_by_username(username)
        instance.ver_code = int(ver_code)
        session.add(instance)
        return instance

    @classmethod
    def confirm_user(cls, username, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_user_by_username(username)
        instance.confirmed = True
        session.add(instance)
        return instance

    @classmethod
    def change(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_user_by_username(username=kwargs["username"])
        instance.firstname = kwargs.get("firstname")
        instance.lastname = kwargs.get("lastname")
        instance.restaurants = kwargs.get("restaurant")
        instance.food = kwargs.get("food")
        tasteid = map(int, kwargs.get("taste"))
        dietid = map(int, kwargs.get("diet"))
        instance.food_profile = []
        instance.diet_restrict = []
        for eid in tasteid:
            instance.food_profile.append(session.query(Profile).filter
                                         (Profile.id == eid).all()[0])
        for eid in dietid:
            instance.diet_restrict.append(session.query(Diet).filter
                                          (Diet.id == eid).all()[0])

        instance.cost = int(kwargs.get("price"))
        instance.user_location = int(kwargs.get("location"))
        instance.age = int(kwargs.get("age"))
        session.add(instance)
        return instance

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Profile(Base, _Table):
    __tablename__ = 'profile'
    taste = Column(Text, unique=True)

    def __repr__(self):
        return "<Taste(%s)>" % (self.taste)


class AgeGroup(Base, _Table):
    __tablename__ = 'agegroup'
    age_group = Column(Text)

    def __repr__(self):
        return "<Age(%s)>" % (self.age_group)


class Location(Base, _Table):
    __tablename__ = 'location'
    city = Column(Text)

    def __repr__(self):
        return "<Location(%s)>" % (self.city)


class Cost(Base, _Table):
    __tablename__ = 'cost'
    cost = Column(Text)

    def __repr__(self):
        return "<Cost(%s)>" % (self.cost)


class Diet(Base, _Table):
    __tablename__ = 'diet'
    diet = Column(Text)

    def __repr__(self):
        return "<Dietary Preference(%s)>" % (self.diet)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))
    discussions = relationship('Discussion',
                               primaryjoin="(Group.id==Discussion.group_id)")

    group_admin = relationship("Admin", uselist=False, backref='group')

    food_profile = relationship('Profile', secondary=grouptaste_table,
                                backref='group')
    diet_restrict = relationship('Diet', secondary=groupdiet_table,
                                 backref='group')
    cost = Column(Integer, ForeignKey('cost.id'))
    age = Column(Integer, ForeignKey('agegroup.id'))
    group_admin = relationship("Admin", uselist=False)

    @classmethod
    def write(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        tasteid = map(int, kwargs.get("food_profile"))
        dietid = map(int, kwargs.get("diet_restrict"))
        grouptaste = []
        diettaste = []
        for eid in tasteid:
            grouptaste.append(session.query(Profile).filter
                              (Profile.id == eid).all()[0])
        for eid in dietid:
            diettaste.append(session.query(Diet).filter
                             (Diet.id == eid).all()[0])
        kwargs["food_profile"] = grouptaste
        kwargs["diet_restrict"] = diettaste
        username = kwargs.get("Admin")
        del kwargs['Admin']
        instance = cls(**kwargs)
        User.addgroup(usergroup=instance, username=username)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all()

    @classmethod
    def lookup_group_by_id(cls, gid, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == gid).one()

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, _Table):
    __tablename__ = 'discussion'
    title = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    posts = relationship('Post',
                         primaryjoin="(Discussion.id==Post.discussion_id)")

    def __repr__(self):
        return "<Discussion(%s)>" % (self.title)


class Post(Base, _Table):
    __tablename__ = 'post'
    text = Column(Text)

    discussion_id = Column(Integer, ForeignKey('discussion.id'))

    def __repr__(self):
        return "<Post(%s)>" % (self.text)


class Admin(Base, _Table):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
