import mysql.connector as mysql
from helpers import error

def member_account_exist(data):
   try:
    connection = mysql.connect (
        host="23.106.53.56",
        user="chakmake_cjadmin",
        password ="Maheshraj##123",
        database="chakmake_cjschool"
        )
    with connection.cursor() as cursor:
        data_query = "SELECT * FROM investors WHERE email = %s AND role = %s"
        cursor.execute(data_query, data)
        row = cursor.fetchone()
        if row == None:
            connection.close()
            return False
        else:
            connection.close()
            return True
   except:
    return error("1001: Error occurred during database connection", 400)

def student_account_exist(data):
    try:
        connection = mysql.connect (
        host="23.106.53.56",
        user="chakmake_cjadmin",
        password ="Maheshraj##123",
        database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM student WHERE email = %s AND role = %s"
            cursor.execute(data_query, data)
            row = cursor.fetchone()
            if row == None:
                connection.close()
                return False
            else:
                connection.close()
                return True
    except:
      return error("1002: Error occurred during database connection", 400)

def staff_account_exist(data):
    try:
        connection = mysql.connect (
        host="23.106.53.56",
        user="chakmake_cjadmin",
        password ="Maheshraj##123",
        database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM staff WHERE email = %s AND role = %s"
            cursor.execute(data_query, data)
            row = cursor.fetchone()
            if row == None:
                connection.close()
                return False
            else:
                connection.close()
                return True
    except:
        return error("1003: Error occurred during database connection", 500)

def admin_account_exist(data):
    try:
        connection = mysql.connect (
        host="23.106.53.56",
        user="chakmake_cjadmin",
        password ="Maheshraj##123",
        database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE email = %s AND role = %s"
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

def retrieve_user_data(data):
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        if data[0] == "investor":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM investors WHERE email = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row
            
        if data[0] == "staff":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM staff WHERE email = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row

        if data[0] == "student":
            return False

        if data[0] == "admin":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM admin WHERE email = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row
        

    except:
        return error("1004: Error occurred during database connection", 400)


def retrieve_user_hash(data):
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        if data[0] == "investor":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM investors WHERE inv_id = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row
            
        elif data[0] == "staff":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM staff WHERE staff_id = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row

        elif data[0] == "student":
            return False
        
        elif data[0] == "admin":
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM admin WHERE admin_id = %s"
                cursor.execute(data_query, (data[1],))
                row = cursor.fetchone()
                if row == None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return row

    except:
        return error("1004: Error occurred during database connection", 400)
