# SPEats - Meal Planning and Recipe Management App

A Python application for meal planning and recipe management.

## Description

SPEats is a meal planning and recipe management application. It allows users to manage recipes, plan meals, and interact with a database of dishes and ingredients.

## Installation

Install the required dependencies using Poetry:

```sh
poetry install
```

## Usage

Run the application using the main.py script:

```sh
python cds_302_project/main.py
```

Use the `--drop-tables` flag to drop existing tables before creating new ones.

## Modules

- main.py: The main program that initializes and runs the application.
- db.py: Contains database models and setup.
- config.py: Defines paths to directories and configuration settings.
- data_handler.py: Reads data from Excel and populates the database.

## Configuration

Configuration settings are defined in config.py. Environment variables are loaded from the `.env` file, which contains database credentials.

## Dependencies

Dependencies are managed using Poetry and specified in `pyproject.toml`. Key dependencies include:

- `sqlalchemy`
- `pandas`
- `python-dotenv`
- `argparse`

## Project Information

This project was developed as part of the CDS 302 (Scientific Data and Databases) course at George Mason University Korea.

**Group Members:**

- Tyson Johnson (<tjohns94@gmu.edu>)
- Giselle Rahimi (<grahimi@gmu.edu>)
- Woohyun Song (<wsong8@gmu.edu>)
- Juheon Kim (<jkim314@gmu.edu>)

**Professor:** Dr. John K. Leung

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2024
Tyson Johnson <tjohns94@gmu.edu>,
Giselle Rahimi <grahimi@gmu.edu>,
Woohyun Song <wsong8@gmu.edu>,
Juheon Kim <jkim314@gmu.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software...
```