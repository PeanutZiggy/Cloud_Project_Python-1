import pandas as pd
import config

# SQL
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

# CSV import
# Team Members: Change your path accordingly as folders can vary.
data_frame = pd.read_csv(
    '/Users/saffanahmed/Documents/Cloud_Project_Python/code/user_credentials.csv')

# SQL Setup: Connecting to the MySQL Server and Creating a Database for Registered Users
connectingSQLServer = mysql.connector.connect(
    host=config.host,
    user=config.username,
    password=config.password)
print(connectingSQLServer)

cursor = connectingSQLServer.cursor()
# Database Entity
db_name = 'db-registeredusers'
