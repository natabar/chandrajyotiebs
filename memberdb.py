import mysql.connector as mysql

def change_investor_pw(data):
    # Update the password in the user table
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            update_query = "UPDATE investors SET hash = %s WHERE inv_id = %s"
            cursor.execute(update_query, data)
            connection.commit()
            connection.close()
        return True
    except:
        return False

def change_admin_pw(data):
    # Update the password in the user table
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            update_query = "UPDATE admin SET hash = %s WHERE admin_id = %s"
            cursor.execute(update_query, data)
            connection.commit()
            connection.close()
        return True
    except:
        return False