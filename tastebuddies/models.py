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

from pyramid.security import Allow
from sqlalchemy_utils.types.choice import ChoiceType

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


user_taste = Table('user_taste', Base.metadata,
                   Column('users', Integer, ForeignKey('users.id')),
                   Column('taste', Integer, ForeignKey('taste.id'))
                   )


user_diet = Table('user_diet', Base.metadata,
                  Column('users', Integer, ForeignKey('users.id')),
                  Column('diet', Integer, ForeignKey('diet.id'))
                  )

group_user = Table('group_user', Base.metadata,
                   Column('groups', Integer, ForeignKey('groups.id')),
                   Column('users', Integer, ForeignKey('users.id'))
                   )

group_taste = Table('group_taste', Base.metadata,
                    Column('group_id', Integer, ForeignKey('groups.id')),
                    Column('taste', Integer, ForeignKey('taste.id'))
                    )


group_diet = Table('group_diet', Base.metadata,
                   Column('group_id', Integer, ForeignKey('groups.id')),
                   Column('diet_id', Integer, ForeignKey('diet.id'))
                   )


class TableSetup(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def add(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    # old groups add method
    # @classmethod
    # def add(cls, session=None, **kwargs):
    #     if session is None:
    #         session = DBSession
    #     taste_id = map(int, kwargs.get("taste"))
    #     diet_id = map(int, kwargs.get("diet"))
    #     grouptaste = []
    #     diettaste = []
    #     for id in taste_id:
    #         grouptaste.append(session.query(Taste).filter
    #                           (Taste.id == id).all()[0])
    #     for id in diet_id:
    #         diettaste.append(session.query(Diet).filter
    #                          (Diet.id == id).all()[0])
    #     kwargs["taste"] = grouptaste
    #     kwargs["diet"] = diettaste
    #     username = kwargs.get("Admin")
    #     del kwargs['Admin']
    #     instance = cls(**kwargs)
    #     User.addgroup(usergroup=instance, username=username)
    #     session.add(instance)
    #     return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all()

    @classmethod
    def lookup_by_attribute(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def edit(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.update(instance)
        return instance


class User(Base, TableSetup):
    __tablename__ = 'users'
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    confirmed = Column(Boolean, default=False)
    ver_code = Column(Integer)
    groups = relationship('Group', secondary=group_user, backref='users')
    restaurants = Column(Text)
    food = Column(Text)
    criteria_id = Column(Integer, ForeignKey('criteria.id'))

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a vaild email address')

    @classmethod
    def addgroup(cls, session=None, usergroup=None, username=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.groups.append(usergroup)
        session.add(instance)
        return instance

    @classmethod
    def write_ver_code(cls, username, ver_code, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.ver_code = int(ver_code)
        session.add(instance)
        return instance

    @classmethod
    def confirm_user(cls, username, session=None):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(username=username)[0]
        instance.confirmed = True
        session.add(instance)
        return instance

    @property
    def __acl__(self):
        acl = []

        acl.append((Allow, self.username, 'owner'))

        for group in self.groups:
            acl.append((Allow, 'group:{}'.format(group.id), 'connect'))

        # acl.append((Deny, Everyone, ALL_PERMISSIONS))

        return acl

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Criteria(Base, TableSetup):
    __tablename__ = 'criteria'
    TASTES = [
        (u'sour', u'Sour'),
        (u'sweet', u'Sweet'),
        (u'salty', u'Salty'),
        (u'spicy', u'Spciy'),
        (u'bitter', u'Bitter'),
        (u'italian', u'Italian'),
        (u'chinese', u'Chinese'),
        (u'american-classic', u'American Classic')
        (u'german', u'German')
        (u'british', u'British'),
        (u'french', u'French'),
        (u'vietnamese', u'Vietnamese'),
        (u'japanese', u'Japanese')
        (u'pub', u'Pub'),
        (u'persian', u'Persian'),
        (u'mediterranian', u'Mediterranian'),
        (u'greek', u'Greek'),
        (u'afghan', u'Afghan'),
        (u'somolian', u'Somolian'),
        (u'thai', u'Thai'),
        (u'barbecue', u'Barbecue')
        (u'soul', u'Soul')
        (u'ethiopian', u'Ethiopian')
        (u'jamaican', u'Jamaican')
        (u'mexican', u'Mexican')
        (u'korean', u'Korean')
    ]
    DIETS = [
        (u'vegetarian', u'Vegetarian'),
        (u'vegan', u'Vegan'),
        (u'gluten-free', u'Gluten Free'),
        (u'low-carb', u'Low Carb')
    ]
    LOCATIONS = [
        (u'seattle', u'Seattle'),
        (u'kitsap', u'Kitsap'),
        (u'eastside', u'Eastside'),
        (u'skagit', u'Skagit'),
        (u'south-king', u'South King')
    ]
    AGES = [
        (u'18-24', u'18-24'),
        (u'25-34', u'25-34'),
        (u'35-44', u'35-44'),
        (u'45-54', u'45-54'),
        (u'55-64', u'55-64'),
        (u'65-74', u'65-74'),
        (u'75+', u'75+')
    ]
    COSTS = [
        (u'$', u'$'),
        (u'$$', u'$$'),
        (u'$$$', u'$$$'),
        (u'$$$$', u'$$$$')
    ]
    taste = Column(ChoiceType(TASTES))
    age = Column(ChoiceType(AGES))
    location = Column(ChoiceType(LOCATIONS))
    cost = Column(ChoiceType(COSTS))
    diet = Column(ChoiceType(DIETS))
    groups = relationship('Group', backref='criteria')
    users = relationship('User', backref='criteria')


class Group(Base, TableSetup):
    __tablename__ = 'groups'
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    discussions = relationship('Discussion',
                               primaryjoin="(Group.id==Discussion.group_id)")
    admin = relationship("Admin", uselist=False)
    criteria_id = Column(Integer, ForeignKey('criteria.id'))

    @classmethod
    def edit(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls.lookup_by_attribute(id=kwargs["id"])[0]
        instance.name = kwargs.get("name")
        instance.description = kwargs.get("description")
        if kwargs.get("discussions"):
            instance.discussions = kwargs.get("discussions")

        session.update(instance)
        return instance

    @classmethod
    def get_members_of_gid(cls, gid, session=None):
        if session is None:
            session = DBSession

        return session.query(User).filter(User.groups == gid).all()

    @property
    def __acl__(self):
        acl = []

        acl.append((Allow, self.admin, 'g_admin'))

        members = self.id.users
        for member in members:
            acl.append((Allow, 'member:{}'.format(member.username), 'member'))

        # acl.append((Deny, Everyone, ALL_PERMISSIONS))

        return acl

    def __repr__(self):
        return "<Group(%s, location=%s)>" % (self.name, self.location)


class Discussion(Base, TableSetup):
    __tablename__ = 'discussion'
    title = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    posts = relationship('Post',
                         primaryjoin="(Discussion.id==Post.discussion_id)")

    def __repr__(self):
        return "<Discussion(%s)>" % (self.title)


class Post(Base, TableSetup):
    __tablename__ = 'post'
    text = Column(Text)
    discussion_id = Column(Integer, ForeignKey('discussion.id'))

    def __repr__(self):
        return "<Post(%s)>" % (self.text)


class Admin(Base, TableSetup):
    __tablename__ = 'admin'
    users = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return "<Admin(%s)>" % (self.users)
