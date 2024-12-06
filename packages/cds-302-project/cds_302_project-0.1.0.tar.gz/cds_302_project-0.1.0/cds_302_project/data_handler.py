import pandas as pd
import logging
from cds_302_project.db import Ingredient, Dish, DishIngredient, DietaryRestriction, IngredientDietaryRestriction, MealType, DishMealType
from cds_302_project.config import log_file, log_level

# Set up logging
logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s %(levelname)s:%(message)s')

class DataHandler:
    def __init__(self, entry_file: str, session):
        self.entry_file = entry_file
        self.session = session
        self.data = {
            "ingredient": self.read_data("ingredient", ["ingredient_id", "name", "calories", "fat", "carbs", "protein", "alcohol", "fiber"]),
            "dish": self.read_data("dish", ["dish_id", "name", "calories", "fat", "carbs", "protein", "alcohol", "fiber"]),
            "dish_ingredient": self.read_data("dish_ingredient", ["dish_id", "ingredient_id", "quantity", "calories", "fat", "carbs", "protein", "alcohol", "fiber"]),
            "dietary_restriction": self.read_data("dietary_restriction", ["restriction_id", "name"]),
            "ingredient_dietary_restriction": self.read_data("ingredient_dietary_restriction", ["ingredient_id", "restriction_id"]),
            "meal_type": self.read_data("meal_type", ["type_id", "name"]),
            "dish_meal_type": self.read_data("dish_meal_type", ["dish_id", "type_id"])
        }

    def read_data(self, sheet_name_var: str, usecols_var: list) -> list:
        dtype_var = {col: int if "id" in col else str for col in usecols_var}
        logging.info(f"Reading data from sheet: {sheet_name_var}")
        return pd.read_excel(self.entry_file, sheet_name=sheet_name_var, usecols=usecols_var, dtype=dtype_var).to_dict('records')

    def create_objects(self):
        def add_record(session, model, record):
            if not session.query(model).get(record['ingredient_id']):
                session.add(model(**record))
            else:
                logging.info(f"Skipping {model.__name__} with ID {record['ingredient_id']} as it already exists.")

        for data in self.data["ingredient"]:
            add_record(self.session, Ingredient, data)
        self.session.commit()

        for data in self.data["dish"]:
            if not self.session.query(Dish).get(data['dish_id']):
                self.session.add(Dish(**data))
            else:
                logging.info(f"Skipping Dish with ID {data['dish_id']} as it already exists.")
        self.session.commit()

        for data in self.data["dietary_restriction"]:
            if not self.session.query(DietaryRestriction).get(data['restriction_id']):
                self.session.add(DietaryRestriction(**data))
            else:
                logging.info(f"Skipping DietaryRestriction with ID {data['restriction_id']} as it already exists.")
        self.session.commit()

        for data in self.data["meal_type"]:
            if not self.session.query(MealType).get(data['type_id']):
                self.session.add(MealType(**data))
            else:
                logging.info(f"Skipping MealType with ID {data['type_id']} as it already exists.")
        self.session.commit()

        for data in self.data["dish_ingredient"]:
            if not self.session.query(DishIngredient).get((data['dish_id'], data['ingredient_id'])):
                self.session.add(DishIngredient(**data))
            else:
                logging.info(f"Skipping DishIngredient with Dish ID {data['dish_id']} and Ingredient ID {data['ingredient_id']} as it already exists.")
        self.session.commit()

        for data in self.data["ingredient_dietary_restriction"]:
            if not self.session.query(IngredientDietaryRestriction).get((data['ingredient_id'], data['restriction_id'])):
                self.session.add(IngredientDietaryRestriction(**data))
            else:
                logging.info(f"Skipping IngredientDietaryRestriction with Ingredient ID {data['ingredient_id']} and Restriction ID {data['restriction_id']} as it already exists.")
        self.session.commit()

        for data in self.data["dish_meal_type"]:
            if not self.session.query(DishMealType).get((data['dish_id'], data['type_id'])):
                self.session.add(DishMealType(**data))
            else:
                logging.info(f"Skipping DishMealType with Dish ID {data['dish_id']} and Type ID {data['type_id']} as it already exists.")
        self.session.commit()
