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
