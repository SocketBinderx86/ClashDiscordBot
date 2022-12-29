import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="St34lth!$OFF",
  database = "801bot",
)

def is_member(clash_tag) -> bool:
  mycursor = mydb.cursor(buffered=True)
  mycursor.execute("select clash_tag from verify")
  found = False
  for item in mycursor.fetchall():
    if clash_tag in item:
      found = True
  mycursor.close()
  return found

def insert_member(discord_name, clash_tag) -> tuple:
  mycursor = mydb.cursor(buffered=True)
  mycursor.execute("select clash_tag from verify")
  for item in mycursor.fetchall():
    if clash_tag in item:
      return False, "Account already linked"
  try:
    mycursor.execute(f"insert into verify(discord_name, clash_tag) values (\"{discord_name}\", \"{clash_tag}\")")
    mydb.commit()
  except:
    return False, "DB failure, please contact admin"
  finally: 
    mycursor.close()
  return True, "success"
  

def print_table(table_name):
  mycursor = mydb.cursor(buffered=True)
  mycursor.execute(f"select * from {table_name}")
  print(mycursor.fetchall())
  mycursor.close()