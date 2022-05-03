# Keepcoding bootcamp final project

Exercise developed using: flask, jinja, DB Browser for SQLite, CSS, coinapi and vscode.

## Description

A record of cryptocurrency movements. 

## Instalation

- Copy `.env_template` and `config_template.py` rename it to `.env` and `config.py` respectively.
- In `.env` file: set your .py file to FLASK_APP (run.py for this application) and choose one of the FLASK_ENV options.
- In `.config` file: 
    - Set the indicated constants (DATABASE_PATH, SECRET_KEY, API_KEY). 
    - Don't change the URL_SPECIFIC_RATE and CURRENCIES constants. 
    - In the CRYPTOCURRENCIES constant you can change the cryptocurrencies codes given by default. 
- The requirements.txt file should list all needed Python libraries, and they will be installed using: 
    ```
    pip install -r requirements.txt
    ```
- The create_table.sql have the SQL CREATE TABLE statement for create the table in a database for this application.

## Author

Adrián Páliz

## Version History

* 0.0.3
    * Release candidate