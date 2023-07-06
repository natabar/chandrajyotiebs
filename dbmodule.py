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
         return True
   except:
      connection.close()
      return False


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
         data_query = "SELECT * FROM investors WHERE email = %s OR mobile = %s"
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

def staff_account_exist_in_db(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "SELECT * FROM staff WHERE email = %s OR mobile = %s"
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

# Pre-register Student
def pre_register_student(data):
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

# Admit New Student
def admit_student_into_db(grade, data):
   try:
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = f"INSERT INTO {grade} (name, full_name_nepali, dob, gender, father_name, father_mobile, mother_name, mother_mobile, address, guardian_name, guardian_mobile, guardian_relation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
         cursor.execute(data_query, data)
         connection.commit()
         connection.close()
         return True
   except:
      return False

def update_student_into_db(std_grade, std_id, data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = f"UPDATE {std_grade} SET name = %s, full_name_nepali = %s, dob = %s, gender = %s, father_name = %s, father_mobile = %s, mother_name = %s, mother_mobile = %s, address = %s, guardian_name = %s, guardian_mobile = %s, guardian_relation = %s WHERE id = {std_id}"
         cursor.execute(data_query, data)
         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
   except Exception as e:
       return e

def AddEventToCalendar(data):
   try:
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         insert_query = "INSERT INTO calendar_events (title, description, type, event_date, everyYear, end_date, color) VALUES(%s, %s, %s, %s, %s, %s, %s)"
         cursor.execute(insert_query, data)
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
         data_query = "INSERT INTO account_access (access_key, mobile_number, account_type) VALUES (%s, %s, %s)"
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

def load_userdata_from_db(user_type):
   try:
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         if user_type == 'bod':
            query = "SELECT * FROM investors"
            cursor.execute(query)
         elif user_type == 'staff':
            query = "SELECT * FROM staff"
            cursor.execute(query)
         result = cursor.fetchall()
         list_mobile = []
         for item in result:
            list_mobile.append(int(item[3]))
         connection.close()
         return list_mobile
   except:
      return False

def load_student_data_from_db(grade_level, std_id):
   try:
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         select_query = f"SELECT * FROM {grade_level} WHERE id = %s"
         cursor.execute(select_query, (std_id,))
         result = cursor.fetchone()
         connection.close()
         return result
   except Exception as e:
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

def insert_staff_into_db(data):
   try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = "INSERT INTO staff (full_name, email, mobile, hash) VALUES (%s, %s, %s, %s)"
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