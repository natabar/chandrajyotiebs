from mysql.connector import errorcode
import mysql.connector

def load_jobs_from_db():
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(user='chakmake_businessdb',
                               password='Maheshraj##123',
                               host='23.106.53.56',
                               database='chakmake_business_profile')
    # Create a cursor object
    cursor = conn.cursor()
    # Execute a SELECT query
    query = ("SELECT * FROM business_profile;")
    cursor.execute(query)
    result = cursor.fetchall()
    # Fetch the results
    jobs = []
    for row in result:
        jobs.append(row)
    # Close the cursor and the connection
    cursor.close()
    conn.close()
    return jobs


def load_job_from_db(id):
  # Establish a connection to the MySQL database
    conn = mysql.connector.connect(user='chakmake_businessdb',
                               password='Maheshraj@#123',
                               host='23.106.53.56',
                               database='chakmake_business_profile')
    # Create a cursor object
    cursor = conn.cursor()
    # Execute a SELECT query
    query = ("SELECT * FROM jobs WHERE id = %s", (id))
    cursor.execute(query)
    result = cursor.fetchall
    rows = result.mappings().all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])