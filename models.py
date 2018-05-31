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




engine = create_engine('sqlite:///fantasybaseball.db')
Base.metadata.create_all(engine)
