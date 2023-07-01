import csv
import mysql.connector as mysql

# connect to mysql remote databse
connection = mysql.connect(
    host="23.106.53.56",
    user="chakmake_cjadmin",
    password ="Maheshraj##123",
    database="chakmake_cjschool"
)
cursor = connection.cursor()
# Open the CSV file
with open('student_data_5.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in reader:
        # Extract student data from the CSV row
        name = row['Student Name']
        dob = row['date of birth']
        father_name = row['father name']
        address = row['Address']
        village = row['Village']
        guardian_mobile = row['mobile number']
        gender = row['Gender']
        
        # SQL query to insert student data into the database
        sql = "INSERT INTO grade_5 (name, dob, gender, father_name, address, guardian_mobile) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, dob, gender, father_name, address, guardian_mobile)
        
        try:
            # Execute the SQL query
            cursor.execute(sql, values)
            
            # Commit the changes to the database
            connection.commit()
            
            print("Student data inserted successfully.")
        except Exception as e:
            # Rollback the transaction in case of any error
            connection.rollback()
            print("Error inserting student data:", e)

# Close the database connection
connection.close()
