import mysql.connector

class MySqlConnection:

  def __init__(self, host, user, password, database):
      self.mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
      )

  def getRecords(self, stmt, size):
      myCursor = self.mydb.cursor(buffered=True)
      myCursor.execute(stmt)
      if (size == 1):
        results = myCursor.fetchone()
      elif (size == 'all'):
        results = myCursor.fetchall()
      else:
        results = myCursor.fetchmany(size)
      return results
