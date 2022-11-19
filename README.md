# FlaskApp

FlaskApp is a web application that manages a user marketplace. The products and the user management is handled by
a MySQL database.

## Installation
Install [Python 3.10.6](https://www.python.org/downloads/release/python-3106/). Afterwards,
use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
$ pip install -r requirements.txt
```

## Restore MySQL Database

To restore the database from the backup, we need a created database in MySQL. To create a database:

```bash
$ mysql -u [username] -p[password] -e "create database [database_name];"
```

Type the following command to restore the database, modifying the parameters as required:
```bash
$ mysql -u [username] -p[password] [database_name] < flask_db.sql
```

Afterwards, change the configuration file [conf.json](conf.json) concerning MySQL, by your system's parameters and
the database name, i.e. [username], [password], [database_name].

## Usage

```bash
$ python app.py
```

## Configuration

Any new configurations must be implemented in [conf.json](conf.json). These configurations include the app
listening PORT and HOST address, and the MySQL server USERNAME, PASSWORD, HOST, PORT, and DB.
