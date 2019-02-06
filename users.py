from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Item(Base):
    __tablename__='item'
    id = Column(Integer, primary_key = True)
    name= Column(String(250), nullable = False)
    img=Column(String(250))
    price=Column(Integer, nullable = False)
    tag = Column(String(250))
    start_date=Column(String(250))
    end_date=Column(String(250))
    description=Column(String(250))
    #user_id=Column(Integer, ForeignKey('user.id'))
    user_id = Column(Integer,ForeignKey('user.id'))
    user=relationship(User)





engine = create_engine('sqlite:///advaitaUsers.db')
Base.metadata.create_all(engine)
