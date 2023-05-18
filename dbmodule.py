import mysql.connector as mysql
from helpers import error

def destroyOTP(access_key):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "DELETE FROM account_access WHERE access_key = %s"
         cursor.execute(data_query, (access_key,))
         connection.commit()
         connection.close()
   except:
      connection.close()


def investor_account_exist(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "SELECT * FROM investors WHERE email = %s AND mobile = %s"
         cursor.execute(data_query, data)
         row = cursor.fetchone()
         if row == None:
            connection.close()
            return False
         else:
            connection.close()
            return True
   except:
      return False

def insert_student_into_db(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "INSERT INTO student (full_name, dob, grade, gender, father_name, father_mobile, mother_name, mother_mobile, p_address, guardian_name, guardian_mobile, guardian_relation, full_name_nepali) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
         cursor.execute(data_query, data)
         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
   except:
       return False

def access_key_into_db(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "INSERT INTO account_access (access_key, account_type) VALUES (%s, %s)"
         cursor.execute(data_query, data)
         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
   
   except Exception as e:
      return error("1005: Error occurred during database connection")

def check_access_key(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "SELECT * FROM account_access WHERE access_key = %s AND account_type = %s"
         cursor.execute(data_query, data)
         row = cursor.fetchone()
         if row == None:
            connection.close()
            return False
         else:
            connection.close()
            return True
   except Exception as e:
      return error("1006: Error occurred during database connection")

def fetch_user(user_id):
   return False

def insert_director_into_db(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "INSERT INTO investors (full_name, email, mobile, hash) VALUES (%s, %s, %s, %s)"
         cursor.execute(data_query, data)

         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
   except:
      return error("1007: Error occurred during database connection")

def transaction_info_into_db(data):
   try:
      connection = mysql.connect (
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "INSERT INTO investment_transactions (inv_id, amount, description, transaction_date, photo) VALUES (%s, %s, %s, %s, %s)"
         cursor.execute(data_query, data)
         # committing transaction
         connection.commit()
         connection.close()
         return True
   except:
      return False