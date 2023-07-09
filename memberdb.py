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

def change_staff_pw(data):
    # Update the password in the user table
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            update_query = "UPDATE staff SET hash = %s WHERE inv_id = %s"
            cursor.execute(update_query, data)
            connection.commit()
            connection.close()
        return True
    except:
        return False

def update_member_profile_into_db(id, data1, data2):
    try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data1_query = f"UPDATE investors_profile SET full_name = %s, education = %s, gender = %s, dob = %s, email = %s, phone_number = %s , address = %s, about_me = %s WHERE inv_id = {id}"
         cursor.execute(data1_query, data1)

         data2_query = f"UPDATE investors_social_media  SET facebook_url = %s, twitter_url = %s, linkedin_url = %s, instagram_url = %s, tiktok_url = %s WHERE inv_id = {id}"
         cursor.execute(data2_query, data2)

         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
    except:
        return False

def update_staff_profile_into_db(id, data1, data2):
    try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data1_query = f"UPDATE staff_profile SET full_name = %s, education = %s, gender = %s, dob = %s, email = %s, phone_number = %s , address = %s, about_me = %s WHERE staff_id = {id}"
         cursor.execute(data1_query, data1)

         data2_query = f"UPDATE staff_social_media  SET facebook_url = %s, twitter_url = %s, linkedin_url = %s, instagram_url = %s, tiktok_url = %s WHERE staff_id = {id}"
         cursor.execute(data2_query, data2)

         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
    except:
        return False