import mysql.connector as mysql

# Connect to MySQL server
connection = mysql.connect(
    host = "23.106.53.56",
    user = "chakmake_cjadmin",
    password = "Maheshraj##123",
    database = "chakmake_cjschool"
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create the staff table
staff_query = """
CREATE TABLE staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  full_name varchar(50) NOT NULL,
  email varchar(25) NOT NULL,
  mobile varchar(15) NOT NULL,
  hash varchar(500) NOT NULL,
  salary decimal(10,0) NOT NULL DEFAULT 1,
  creation_time datetime DEFAULT current_timestamp(),
  modification_time datetime DEFAULT NULL ON UPDATE current_timestamp(),
  role varchar(20) DEFAULT 'staff',
  designation varchar(30) DEFAULT NULL,
  address varchar(50) DEFAULT NULL
)
"""
cursor.execute(staff_query)
connection.commit()

# Create the staff_profile table
create_table_query = """
CREATE TABLE staff_profile (
    id INT PRIMARY KEY NOT NULL,
    staff_id INT,
    full_name varchar(50),
    designation varchar(50),
    education varchar(50),
    gender varchar(10),
    dob date,
    email varchar(30),
    phone_number varchar(15),
    address varchar(150),
    about_me varchar(2000),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
)
"""

# Execute the create table query
cursor.execute(create_table_query)
connection.commit()


# Create the staff_social_media table
create_table_query = """
CREATE TABLE staff_social_media (
    id INT PRIMARY KEY NOT NULL,
    staff_id INT,
    facebook_url varchar(50),
    twitter_url varchar(50),
    linkedin_url varchar(50),
    instagram_url varchar(50),
    tiktok_url varchar(50),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
)
"""

# Execute the create table query
cursor.execute(create_table_query)
connection.commit()


# Create a trigger to insert a row into staff_profile whenever a new staff member is added to the staff table
create_trigger_query = """
CREATE TRIGGER insert_staff_profile AFTER INSERT ON staff
FOR EACH ROW
BEGIN
    INSERT INTO staff_profile (id, staff_id)
    VALUES (NEW.staff_id, NEW.staff_id);
    INSERT INTO staff_social_media (id, staff_id)
    VALUES (NEW.staff_id, NEW.staff_id);
END
"""

# Execute the create trigger query
cursor.execute(create_trigger_query)
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
print("Success!")