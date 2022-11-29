import mysql.connector

def connect(host, user, password, database):
  return mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database,
  )

def execute(cursor, sql):
  return cursor.execute(sql)

