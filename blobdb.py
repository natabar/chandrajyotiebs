import mysql.connector as mysql

def InsertBlob(data):
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection as cnx:
            cursor = cnx.cursor()
            data_query = "INSERT INTO investment_transactions (inv_id, amount, description, transaction_date, photo, image_format) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(data_query, data)
            cnx.commit()
            connection.close()
            return True
    except:
        return error("1006: Error occurred")

# Insert Notice Data
def InsertNotice(data):
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection as cnx:
            cursor = cnx.cursor()
            data_query = "INSERT INTO newsandupdates (title, content, filepath) VALUES (%s, %s, %s)"
            cursor.execute(data_query, data)
            cnx.commit()
            connection.close()
            return True
    except:
        return error("1006: Error occurred")

def retrieve_image_from_db (id, image_data, image_format):
    # Specify the file path
    file_path = f"static/image_gallery/img{id}.{image_format}"
    # Save the image data to a file
    with open(file_path, "wb") as file:
            file.write(image_data)
    return True

def retrieve_staff_photo_from_db (id, image_data, image_format):
    # Specify the file path
    file_path = f"static/staff-profile/img{id}.{image_format}"
    # Save the image data to a file
    with open(file_path, "wb") as file:
            file.write(image_data)
    return True

def retrieve_investor_photo_from_db (id, image_data, image_format):
    # Specify the file path
    file_path = f"static/investors-profile/img{id}.{image_format}"
    # Save the image data to a file
    with open(file_path, "wb") as file:
            file.write(image_data)
    return True

def update_member_profile_picture(id, data):
    try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = f"UPDATE investors_profile SET photo = %s, img_format = %s WHERE inv_id = {id}"
         cursor.execute(data_query, data)

         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
    except:
        return False

def update_staff_profile_picture(id, data):
    try:
      # connect to mysql remote databse
      connection = mysql.connect(
         host="23.106.53.56",
         user="chakmake_cjadmin",
         password ="Maheshraj##123",
         database="chakmake_cjschool"
      )
      with connection.cursor() as cursor:
         data_query = f"UPDATE staff_profile SET photo = %s, img_format = %s WHERE staff_id = {id}"
         cursor.execute(data_query, data)

         # Commit the changes to the database
         connection.commit()
         connection.close()
         return True
    except:
        return False