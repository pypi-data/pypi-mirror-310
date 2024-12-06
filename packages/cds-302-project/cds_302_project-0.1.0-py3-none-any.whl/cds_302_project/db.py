"""
This file contains classes that represent the tables in the database. 
Each class represents a table in the database and has attributes that correspond to the columns in the table.
The classes also have methods that can be used to interact with the database.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from contextlib import contextmanager
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

class Database:
    def __init__(self, address):
        self.engine = create_engine('sqlite:///' + address.as_posix())
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def create_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        list_of_table_names = ['dish', 'ingredient', 'dish_ingredient', 'dietary_restriction', 'ingredient_dietary_restriction', 'meal_type', 'dish_meal_type'][::-1]
        for table_name in list_of_table_names:
            Base.metadata.tables[table_name].drop(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

# Define database models
class Ingredient(Base):
    __tablename__ = 'ingredient'
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(64))
    calories = Column(Numeric(10,2))
    fat = Column(Numeric(10,2))
    carbs = Column(Numeric(10,2))
    protein = Column(Numeric(10,2))
    alcohol = Column(Numeric(10,2))
    fiber = Column(Numeric(10,2))

class Dish(Base):
    __tablename__ = 'dish'
    dish_id = Column(Integer, primary_key=True)
    name = Column(String(64))
    calories = Column(Numeric(10,2))
    fat = Column(Numeric(10,2))
    carbs = Column(Numeric(10,2))
    protein = Column(Numeric(10,2))
    alcohol = Column(Numeric(10,2))
    fiber = Column(Numeric(10,2))
    ingredients = relationship("DishIngredient", back_populates="dish")

class DishIngredient(Base):
    __tablename__ = 'dish_ingredient'
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'), primary_key=True)
    quantity = Column(Numeric(10,2))
    calories = Column(Numeric(10,2))
    fat = Column(Numeric(10,2))
    carbs = Column(Numeric(10,2))
    protein = Column(Numeric(10,2))
    alcohol = Column(Numeric(10,2))
    fiber = Column(Numeric(10,2))
    dish = relationship("Dish", back_populates="ingredients")
    ingredient = relationship("Ingredient")

class DietaryRestriction(Base):
    __tablename__ = 'dietary_restriction'
    restriction_id = Column(Integer, primary_key=True)
    name = Column(String(64))

class IngredientDietaryRestriction(Base):
    __tablename__ = 'ingredient_dietary_restriction'
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'), primary_key=True)
    restriction_id = Column(Integer, ForeignKey('dietary_restriction.restriction_id'), primary_key=True)

class MealType(Base):
    __tablename__ = 'meal_type'
    type_id = Column(Integer, primary_key=True)
    name = Column(String(64))

class DishMealType(Base):
    __tablename__ = 'dish_meal_type'
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('meal_type.type_id'), primary_key=True)
