"""
This file contains the configuration settings for the project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define directories
working_dir = Path.cwd() / "cds_302_project"
data_dir = working_dir / "data"
output_dir = working_dir / "output"
logs_dir = output_dir / "logs"
entry_file = data_dir / "food_data.xlsx"

# This is for publishing online, requires environment variables to be set
# from sqlalchemy import engine
# database_file = engine.URL.create(
#         host=os.getenv('env_HOST'),
#         database=os.getenv('env_DATABASE'),
#         username=os.getenv('env_USER'),
#         password=os.getenv('env_PASS'), 
#         drivername=os.getenv('env_DRIVER')
#     )

database_file = data_dir / "cds302.db"

# Ensure all directories exist
data_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)
logs_dir.mkdir(parents=True, exist_ok=True)

# Logging configuration
log_file = logs_dir / 'data_handler.log'
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()