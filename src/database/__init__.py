from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from discord.user import User as DiscordUser
from .models import User, Item, user_item_association
from .models.base import Base
from enum import Enum
import sqlite3

class BalanceLocation(Enum):
    BANK = "bank"
    CASH = "cash"

class NotEnoughBalance(Exception):
    pass

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
            last_collected_income: int = None,
            last_worked: int = None,
            last_slutted: int = None,
            last_crimed: int = None
        ) -> User:
        if direct_to_bank:
            user.bank += amount
        else:
            user.cash += amount

        if last_collected_income != None: user.last_collected_income = last_collected_income
        if last_worked != None: user.last_worked = last_worked
        if last_slutted != None: user.last_slutted = last_slutted
        if last_crimed != None: user.last_crimed = last_crimed

        self.session.commit()
        return user
    
    def deduct_user_balance(
            self,
            user: User,
            amount: int
    ):
        user.cash -= amount
        self.session.commit()
        return user
    
    def add_user_xp(
            self,
            user: User,
            normal_xp: int = 0,
            job_xp: int = 0
        ) -> User:

        user.job_xp += job_xp

        self.session.commit()
        return user
    
    def transfer_balance(
            self,
            user: User,
            to: BalanceLocation,
            amount: int
        ) -> User:
        if to == BalanceLocation.CASH:
            if amount <= user.bank:
                user.bank -= amount
                user.cash += amount
            else:
                raise NotEnoughBalance()
        elif to == BalanceLocation.BANK:
            if amount <= user.cash:
                user.cash -= amount
                user.bank += amount
            else:
                raise NotEnoughBalance()
        
        self.session.commit()
        return user

    def get_account_from_enum(self, user: User, acc_type: BalanceLocation) -> int:
        if acc_type == BalanceLocation.BANK: return user.bank
        else: return user.cash

    def get_all_items(self) -> list:
        items = self.session.query(Item).all()
        return items
    
    def create_item(self, name: str, description: str, price: int) -> Item:
        item = Item(
            name=name,
            description=description,
            price=price
        )
        self.session.add(item)
        self.session.commit()
        return item
    
    def get_user_items(self, user: User) -> list:
        items = user.items
        return items
    
    def add_item_to_user_inventory(self, user: User, item: Item, quantity: int = 1) -> User:
        if item in user.items:
            user_item = self.session.query(user_item_association).filter_by(
                user_id=user.id, item_id=item.id
            ).first()
            user_item.quantity += quantity
        else:
            user.items.append(item)
            user_item = self.session.query(user_item_association).filter_by(
                user_id=user.id, item_id=item.id
            ).first()
            user_item.quantity = quantity

        self.session.commit()
        return user

    def remove_item_from_user_inventory(self, user: User, item: Item, quantity: int = 1) -> User:
        if item in user.items:
            user_item = self.session.query(user_item_association).filter_by(
                user_id=user.id, item_id=item.id
            ).first()

            if user_item.quantity <= quantity:
                user.items.remove(item)
                self.session.delete(user_item)
            else:
                user_item.quantity -= quantity

            self.session.commit()
        return user
    
    def create_user_item(self, user: User, name: str, description: str, price: int) -> Item:
        item = Item(name=name, description=description, price=price, creator=user)
        self.session.add(item)
        self.session.commit()
        return item