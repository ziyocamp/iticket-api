from sqlalchemy import(
    Column,
    Integer, 
    String, 
    Text, 
    Boolean, 
    ForeignKey, 
    DateTime, 
    VARCHAR, 
    CheckConstraint, 
    TIMESTAMP,
    DECIMAL,
    func
    
) 

from app.db.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,)
    username = Column(VARCHAR(100), unique=True, nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    phone = Column(VARCHAR(15), unique=True)
    password = Column(VARCHAR(225), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0'))
    role = Column(VARCHAR(10), nullable=False, default='user')
    created_at = Column(TIMESTAMP, server_default=func.now())

class Venues(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True,)
    name = Column(VARCHAR(100), unique=True, nullable=False)
    lon = Column(DECIMAL(9,6), nullable=False)
    lat = Column(DECIMAL(9,6), nullable=False)
class Events(Base):
    __tablename__ = 'events'
    id = Column(VARCHAR(150), primary_key=True,)
    name = Column(VARCHAR(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    limit_age = Column(Integer, CheckConstraint('limit_age >= 0'))
    venue_id = Column(Integer, ForeignKey('venues.id', ondelete='CASCADE'))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)

class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True,)
    name = Column(VARCHAR(100), nullable=False)
    event_id = Column(VARCHAR(150), ForeignKey('events.id', ondelete='CASCADE'))
    price = Column(DECIMAL(10,2), nullable=False)
    quantity = Column(Integer, CheckConstraint('quantity >= 0'), nullable=False)

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True,)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    ticket_id = Column(Integer, ForeignKey('tickets.id', ondelete='CASCADE'))
    quantity = Column(Integer, CheckConstraint('quantity > 0'), nullable=False)
    total_price = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    