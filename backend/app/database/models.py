from sqlalchemy import Column, Integer, String, Text

from backend.app.database.database import Base


class UserProfileDB(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    interests = Column(Text, nullable=True)


class ChatHistoryDB(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    role = Column(String)
    message = Column(Text)