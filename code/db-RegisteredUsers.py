# Prequisite Modules
import os
import pandas as pd
import config

# SQL
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

# CSV import
# Team Members: Change your path accordingly as folders can vary.
df = pd.read_csv(os.path.join('users.csv'))

# SQL Setup: Connecting to the MySQL Server and Creating a Database for Registered Users
connectingSQLServer = mysql.connector.connect(
    host=config.host,
    user=config.username,
    password=config.password)
print(connectingSQLServer)

cursor = connectingSQLServer.cursor()
# Database Entity
db_name = 'users'

# Creating the Database


def database_create(cursor, database):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(db_name))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(db_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        database_create(cursor, db_name)
        print("Database {} created successfully.".format(db_name))
        connectingSQLServer.database = db_name
    else:
        print(err)
        exit(1)

connectingSQLServer.commit()
cursor.close()
connectingSQLServer.close()

SQL_Engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}"
                           .format(user=config.username,
                                   pw=config.password,
                                   host=config.host,
                                   db=config.db_name))

# Inserting entire DataFrame into MySQL Server.
df.to_sql('users', con=SQL_Engine, if_exists='append')
