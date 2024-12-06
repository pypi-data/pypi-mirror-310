"""
SPEats - a meal planning and recipe management app

Modules:
- main.py: main program
- db.py: database models and setup
- config.py: paths to directories and configuration settings
- data_handler.py: reads data from Excel and populates the database

To run the program, execute main.py in the terminal.

=======================

Author: Tyson Johnson
Date: 2024-06-25
Version: 1.0
"""

import argparse
from cds_302_project.db import Database
from cds_302_project.data_handler import DataHandler
from cds_302_project.config import database_file, entry_file

def main(drop_tables=False):
    # Define database
    sp_eats_db = Database(database_file)
    #sp_eats_db.create_db()

    with sp_eats_db.session_scope() as session:
        if drop_tables:
            # Drop tables if they exist (only in development or testing)
            sp_eats_db.drop_tables()

        # Create tables if they don't exist
        sp_eats_db.create_tables()

        # Create objects and populate the database
        data_handler = DataHandler(entry_file, session)
        data_handler.create_objects()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SPEats - Meal Planning and Recipe Management App')
    parser.add_argument('--drop-tables', action='store_true', help='Drop tables before creating them')
    args = parser.parse_args()

    main(drop_tables=args.drop_tables)
