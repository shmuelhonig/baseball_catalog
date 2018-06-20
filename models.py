from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import random
import string

Base = declarative_base()

# should I change the name of this key????
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                     x in xrange(32))


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    name = Column(String(100), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }


class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(6))
    number = Column(String(2))
    handedness = Column(String(1))
    team_id = Column(Integer, ForeignKey('teams.id'))
    teams = relationship(Teams)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'number': self.number,
            'handedness': self.handedness,
            'team_id': self.team_id,
            'user_id': self.user_id
        }

engine = create_engine('sqlite:///baseball.db')
Base.metadata.create_all(engine)
