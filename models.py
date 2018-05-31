from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
	__tablename__ = 'users'

    id = Column(Integer, primary_key=True)
	email = Column(String(50))
	username = Column(String(100), nullable=False)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'email': self.email,
			'username': self.username
		}


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




engine = create_engine('sqlite:///baseball.db')
Base.metadata.create_all(engine)
