from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from discord.user import User as DiscordUser
from .models import User
from .models.base import Base
import sqlite3

class Database:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.sqlite", echo=True)
        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        pass

    def add_user(self, discord_user: DiscordUser) -> User:
        user = User(
            id=discord_user.id,
            discord_username=discord_user.name,
            balance=0
        )

        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, discord_user: DiscordUser) -> User:
        try:
            user = self.session.query(User).filter_by(User.id == discord_user.id).first()
        except:
            self.session.rollback()
            user = self.add_user(discord_user)

        print(user)
        return user