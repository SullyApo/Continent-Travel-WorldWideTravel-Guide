from sqlalchemy import Boolean, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.orm import relationship
from sqlalchemy import Column, JSON


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(300))
    is_active = Column(Boolean, default=True)
    
    favorites = relationship("UserFavorite", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), nullable=False)
    answer = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String(100))
    
    user = relationship("User", back_populates="chat_history")

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    price_range = Column(String(50))
    country = Column(String(100))
    climate = Column(String(50))
    activities = Column(String(200))
    image_url = Column(String(300))
    
    favorites = relationship("UserFavorite", back_populates="destination")

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    
    user = relationship("User", back_populates="favorites")
    destination = relationship("Destination", back_populates="favorites")

Index("idx_created_at", ChatHistory.created_at)

class FlightBooking(Base):
    __tablename__ = "flight_bookings"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    itinerary_id = Column(String(50), nullable=False)
    passengers = Column(JSON)  # Stockage des détails passagers
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")
    expires_at = Column(DateTime)
    payment_reference = Column(String(100))
    
    user = relationship("User", back_populates="flight_bookings")

class Hebergement(Base):
    __tablename__ = "hebergements"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    type_hebergement = Column(String(50))  # hôtel, auberge, Airbnb...
    adresse = Column(String(200))
    ville = Column(String(100))
    pays = Column(String(100))
    prix_nuit = Column(Float)
    capacite = Column(Integer)
    equipements = Column(Text, nullable=True)
    note_moyenne = Column(Float, nullable=True)
    image_url = Column(String(300), nullable=True)
    
    # Relation avec les favoris si nécessaire
    favorites = relationship("UserFavorite", back_populates="hebergement")