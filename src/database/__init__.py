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
            discord_username=discord_user.name
        )

        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, discord_user: DiscordUser) -> User:
        try:
            user = self.session.query(User).filter(User.id == discord_user.id).first()
            assert user != None
        except:
            self.session.rollback()
            user = self.add_user(discord_user)
        return user
    
    def add_to_user_balance(
            self, 
            user: User, 
            amount: int, 
            direct_to_bank: bool = False,
            last_collected_income: int = None
        ) -> User:
        if direct_to_bank:
            user.bank += amount
        else:
            user.cash += amount

        if last_collected_income != None:
            user.last_collected_income = last_collected_income

        self.session.commit()
        return user