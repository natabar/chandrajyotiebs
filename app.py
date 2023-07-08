from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from dotenv import load_dotenv
import os, base64
import secrets
from flask_session import Session
from dbmodule import load_userdata_from_db, load_student_data_from_db, admit_student_into_db, update_staff_into_db, update_student_into_db, pre_register_student, AddEventToCalendar, check_access_key, investor_account_exist, staff_account_exist_in_db, insert_director_into_db, insert_staff_into_db, access_key_into_db, transaction_info_into_db, destroyOTP
from database import load_job_from_db, load_jobs_from_db, load_notices_from_db, load_notice_from_db
from memberdb import change_investor_pw, change_admin_pw, change_staff_pw, update_member_profile_into_db, update_staff_profile_into_db
from userdb import staff_account_exist, member_account_exist, student_account_exist, admin_account_exist, retrieve_user_data, retrieve_user_hash
from helpers import error, admin_error, staff_error, success, admin_success, staff_success, login_required, admin_login_required, member_login_required, staff_login_required, student_login_required, number_validity, check_sms_system_bal, SMS_sociair, multiple_sms, has_expired, npr, TrunDecimal, convert_date
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
import mysql.connector as mysql
from werkzeug.utils import secure_filename
import urllib.request
from blobdb import InsertBlob, retrieve_image_from_db, retrieve_investor_photo_from_db, retrieve_staff_photo_from_db, InsertNotice
import imghdr
import json

def configure():
    load_dotenv()

#application setup
app = Flask(__name__)

#secrete key during deployment
app.secret_key = os.getenv("secrete_key")

# ensuring template autoreloading
app.config["TEMPLATES_ATUO_RELOAD"] = True

# Use filesystem for session instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    session.clear()
    """Login user"""
    if request.method == "POST":
        account_type = request.form.get("account_type")
        email = request.form.get("email")
        if not email or not account_type:
            return error("Missing Input field such as email and account type", 400)
        
        data = (email, account_type)
        # To continue as Board Member
        if account_type == "investor":
            isexist = member_account_exist(data)
            if isexist == False:
                return error("Invalid Email.", 400)
            elif isexist == True:
                return render_template('login-continue.html', data = data)
            else:
                return error(isexist, 1010)
        
        # To continue as Student
        elif account_type == "student":
            isexist = student_account_exist(data)
            if isexist == False:
                return error("Invalid Email.", 400)
            elif isexist == True:
                return render_template('login-continue.html', data = data)
            else:
                return error("No such user found.", 1011)

        # To continue as Staff
        elif account_type == "staff":
            isexist = staff_account_exist(data)
            if isexist == False:
                return error("Invalid Email.", 400)
            elif isexist == True:
                return render_template('login-continue.html', data = data)
            else:
                return error(isexist, 1012)
        
        # To continue as Admin
        elif account_type == "admin":
            isexist = admin_account_exist(data)
            if isexist == False:
                return error("Invalid Email.", 400)
            elif isexist == True:
                return render_template('login-continue.html', data = data)
            else:
                return error("Database Issue", 1012.1)
    else:
        return render_template("login.html")


@app.route("/login-continue", methods = ["POST"])
def login_continue():
    if request.method == "POST":
        account_type = request.form.get("account_type")
        email = request.form.get("email")
        if not account_type or not email:
            return error("Missing Form Data", 400)
        password = request.form.get("password")
        if not password:
            return error("Password is required")
        
        data = (account_type, email)
        row = retrieve_user_data(data)
        if row:
            # for investor
            if account_type == "investor":
                if check_password_hash(row[4], password):
                    #Remember which user has logged in
                    session["member_id"] = row[0]
                    session["loggedin"] = True
                    #Redirect user to dashboard
                    return redirect("/dashboard")
                else:
                    return error("Invalid password", 400)
            
            # for staff
            elif account_type == "staff":
                if check_password_hash(row[4], password):
                    #Remember which user has logged in
                    session["staff_id"] = row[0]
                    session["loggedin"] = True
                    #Redirect user to dashboard
                    return redirect("/staff")
                else:
                    return error("Invalid password", 400)
            
            # for student
            elif account_type == "student":
                if check_password_hash(row[4], password):
                    #Remember which user has logged in
                    session["std_id"] = row[0]
                    session["loggedin"] = True
                    #Redirect user to dashboard
                    return redirect("/dashboard")
                else:
                    return error("Invalid password", 400)

            # for admin
            elif account_type == "admin":
                if check_password_hash(row[4], password):
                    #Remember which user has logged in
                    session["admin_id"] = row[0]
                    session["loggedin"] = True
                    #Redirect user to dashboard
                    return redirect("/admin")
                else:
                    return error("Invalid password", 400)
            else:
                return error("Check your account type and try in a moment", 400)

        else:
            return error("invalid password", 400)
    else:
        return error("We can’t find a page with the url you entered.", 400)

# ###################### Member route ############################
@app.route("/dashboard")
@member_login_required
def dashboard():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            # fetch data of logged in User
            data_query = "SELECT * FROM investors WHERE inv_id = %s"
            cursor.execute(data_query, (session["member_id"],))
            row = cursor.fetchone()
            # fetch total investment cash from investors
            data_query = "SELECT sum(cash) FROM investors"
            cursor.execute(data_query)
            row2 = cursor.fetchall()
            # fetch all investment transaction
            data_query = "SELECT * FROM investment_transactions"
            cursor.execute(data_query)
            row3 = cursor.fetchall()

            cursor.execute("SELECT count(*) FROM investors")
            inv_count = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM staff")
            staff_count = cursor.fetchone()

            cursor.execute("SELECT (SELECT COUNT(*) FROM grade_nursery) + (SELECT COUNT(*) FROM grade_LKG) + (SELECT COUNT(*) FROM grade_UKG) + (SELECT COUNT(*) FROM grade_1) + (SELECT COUNT(*) FROM grade_2) + (SELECT COUNT(*) FROM grade_3) + (SELECT COUNT(*) FROM grade_4) + (SELECT COUNT(*) FROM grade_5) AS total_students_all_grades;")
            std_count = cursor.fetchone()

            connection.close()
            # retrieve Image from DB
            for each_row in row3:
                id = str(each_row[0])
                image_data = each_row[5]
                image_format = each_row[6]
                retrieve_image_from_db (id, image_data, image_format)
            # enumerate template data
            cash = row[5]
            shares = TrunDecimal(cash/100000)
            percent = (cash/row2[0][0])*100
            template_data = {
                'username' : row[1],
                'amount' : npr(cash),
                'shares' : shares,
                'percent' : TrunDecimal(percent),
                'transaction' : row3,
                'inv_count' : inv_count[0],
                'staff_count' : staff_count[0],
                'std_count' : std_count[0]
             }
        return render_template("dashboard.html", **template_data)
    except:
        return "1008: Error occurred during database connection"

######################## Admin Route #########################
@app.route("/admin")
@admin_login_required
def admin():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE admin_id = %s"
            cursor.execute(data_query, (session["admin_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM investors")
            inv_count = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM staff")
            staff_count = cursor.fetchone()

            cursor.execute("SELECT (SELECT COUNT(*) FROM grade_nursery) + (SELECT COUNT(*) FROM grade_LKG) + (SELECT COUNT(*) FROM grade_UKG) + (SELECT COUNT(*) FROM grade_1) + (SELECT COUNT(*) FROM grade_2) + (SELECT COUNT(*) FROM grade_3) + (SELECT COUNT(*) FROM grade_4) + (SELECT COUNT(*) FROM grade_5) AS total_students_all_grades;")
            std_count = cursor.fetchone()

            connection.close()
            template_data = {
                'username' : row[1],
                'inv_count' : inv_count[0],
                'staff_count' : staff_count[0],
                'std_count' : std_count[0],
                'sms_system_bal' : check_sms_system_bal()
            }
            return render_template("admin.html", **template_data)
    except Exception as e:
        return admin_error(e, 404)

# search handling for specific student 
@app.route("/std_info", methods = ["POST", "GET"])
@admin_login_required
def get_std_info():
    if request.method == "POST":
        std_name = request.form.get("std_name")
        user_staff = request.form.get("user_staff")
        if not std_name and not user_staff:
            return admin_error("input data cannot be empty!", 400)
        split_word = std_name.split()
        grade_level = split_word[-1]
        std_id = int(split_word[0])

        # check if user exists
        try:
            connection = mysql.connect (
                host = "23.106.53.56",
                user = "chakmake_cjadmin",
                password = "Maheshraj##123",
                database = "chakmake_cjschool"
            )
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM admin WHERE admin_id = %s"
                cursor.execute(data_query, (session["admin_id"],))
                row = cursor.fetchone()

                cursor.execute("SELECT count(*) FROM investors")
                inv_count = cursor.fetchone()

                cursor.execute("SELECT count(*) FROM staff")
                staff_count = cursor.fetchone()

                cursor.execute("SELECT (SELECT COUNT(*) FROM grade_nursery) + (SELECT COUNT(*) FROM grade_LKG) + (SELECT COUNT(*) FROM grade_UKG) + (SELECT COUNT(*) FROM grade_1) + (SELECT COUNT(*) FROM grade_2) + (SELECT COUNT(*) FROM grade_3) + (SELECT COUNT(*) FROM grade_4) + (SELECT COUNT(*) FROM grade_5) AS total_students_all_grades;")
                std_count = cursor.fetchone()

                cursor.execute("SELECT * FROM grade_nursery")
                std_nursery = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_LKG")
                std_LKG = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_UKG")
                std_UKG = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_1")
                std_1 = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_2")
                std_2 = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_3")
                std_3 = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_4")
                std_4 = cursor.fetchall()

                cursor.execute("SELECT * FROM grade_5")
                std_5 = cursor.fetchall()

                selected_std = load_student_data_from_db(grade_level, std_id)


                connection.close()
                template_data = {
                    'username' : row[1],
                    'inv_count' : inv_count[0],
                    'staff_count' : staff_count[0],
                    'std_count' : std_count[0],
                    'std_nursery' : std_nursery,
                    'std_LKG' : std_LKG,
                    'std_UKG' : std_UKG,
                    'std_1' : std_1,
                    'std_2' : std_2,
                    'std_3' : std_3,
                    'std_4' : std_4,
                    'std_5' : std_5,
                    'selected_std' : selected_std,
                    'grade_level' : grade_level
                }
                return render_template("student-info.html", **template_data)
        except Exception as e:
            return admin_error(e, 404)
    else:
        return error("Aunauthorized Access Attempt!", 400)

# search handling for specific staff 
@app.route("/get-staff-info", methods = ["POST", "GET"])
@admin_login_required
def get_staff_info():
    if request.method == "POST":
        user_staff = request.form.get("staff_name")
        if not user_staff:
            return admin_error("input data cannot be empty!", 400)
        split_word = user_staff.split()
        staff_id = int(split_word[0])

        # check if user exists
        try:
            connection = mysql.connect (
                host = "23.106.53.56",
                user = "chakmake_cjadmin",
                password = "Maheshraj##123",
                database = "chakmake_cjschool"
            )
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM admin WHERE admin_id = %s"
                cursor.execute(data_query, (session["admin_id"],))
                row = cursor.fetchone()

                cursor.execute("SELECT * FROM staff")
                staff_all = cursor.fetchall()

                data_query = f"SELECT * FROM staff WHERE staff_id = {staff_id}"
                cursor.execute(data_query)
                selected_staff = cursor.fetchone()

                connection.close()
                template_data = {
                    'username' : row[1],
                    'staff_all' : staff_all,
                    'selected_staff' : selected_staff
                }
            return render_template("staff-info.html", **template_data)
        except Exception as e:
            return admin_error(e, 404)
    else:
        return error("Unauthorized Access Attempt!", 400)

# Update Student Details
@app.route("/update_student", methods = ["POST"])
@admin_login_required
def update_student():
    if request.method == "POST":
        std_tag = request.form.get("id")
        full_name = request.form.get("full_name")
        full_name_nepali = request.form.get("full_name_nepali")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        father_name = request.form.get("father_name")
        father_mobile = request.form.get("father_mobile")
        mother_name = request.form.get("mother_name")
        mother_mobile = request.form.get("mother_mobile")
        p_address = request.form.get("p_address")
        guardian_name = request.form.get("guardian_name")
        guardian_mobile = request.form.get("guardian_mobile")
        guardian_relation = request.form.get("guardian_relation")

        if not std_tag or not full_name or not dob or not father_name or not mother_name or not p_address or not guardian_name or not guardian_mobile or not guardian_relation:
            return admin_error("Your form seems to be Incomplete. Please recheck your form and submit AGAIN", 400)
        split_word = std_tag.split()
        std_id = split_word[0]
        std_grade = split_word[-1]

        data = (full_name, full_name_nepali, dob, gender, father_name, father_mobile, mother_name, mother_mobile, p_address, guardian_name, guardian_mobile, guardian_relation)
        # update to DB
        is_updated = update_student_into_db(std_grade, std_id, data)
        if is_updated == True:
            return admin_success("Student data updated successfully")
        else:
            return admin_error("Could not update the data", 400)

# Update Staff Details
@app.route("/update_staff", methods = ["POST"])
@admin_login_required
def update_staff():
    if request.method == "POST":
        staff_id = request.form.get("id")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        designation = request.form.get("designation")
        class_assigned = request.form.get("class_assigned")

        if not id or not email or not mobile or not designation:
            return admin_error("Required field cannot be empty", 400)

        data = (email, mobile, designation, class_assigned)
        # update to DB
        is_updated = update_staff_into_db(staff_id, data)
        if is_updated == True:
            return admin_success("Staff data updated successfully")
        else:
            return admin_error("Could not update the data", 400)

# Admin SMS
@app.route("/admin-sms")
@admin_login_required
def admin_sms():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE admin_id = %s"
            cursor.execute(data_query, (session["admin_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM investors")
            inv_count = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM staff")
            staff_count = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM student")
            std_count = cursor.fetchone()

            cursor.execute("SELECT * FROM investors")
            inv_all = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_nursery")
            std_nursery = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_LKG")
            std_LKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_UKG")
            std_UKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_1")
            std_1 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_2")
            std_2 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_3")
            std_3 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_4")
            std_4 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_5")
            std_5 = cursor.fetchall()

            cursor.execute("SELECT * FROM sms_syntax")
            sms_syntax = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_nursery UNION SELECT * FROM grade_LKG UNION SELECT * FROM grade_UKG UNION SELECT * FROM grade_1 UNION SELECT * FROM grade_2 UNION SELECT * FROM grade_3 UNION SELECT * FROM grade_4 UNION SELECT * FROM grade_5")
            std_all = cursor.fetchall()

            connection.close()
        template_data = {
            'username' : row[1],
            'inv_count' : inv_count[0],
            'staff_count' : staff_count[0],
            'std_count' : std_count[0],
            'inv_all' : inv_all,
            'std_nursery' : std_nursery,
            'std_LKG' : std_LKG,
            'std_UKG' : std_UKG,
            'std_1' : std_1,
            'std_2' : std_2,
            'std_3' : std_3,
            'std_4' : std_4,
            'std_5' : std_5,
            'sms_syntax' : sms_syntax,
            'std_all' : std_all
        }
        return render_template("sms.html", **template_data)
    except Exception as e:
        return admin_error(e, 404)

# Send multiple SMS to people
@app.route("/bulk_sms", methods=["POST"])
@admin_login_required
def bulk_sms():
    if request.method == 'POST':
        audience_type = request.form.get('audience_type')
        message = request.form.get('content')
        if not audience_type or not message:
            return admin_error("Recipient and/or message missing!", 400)
        user_data = load_userdata_from_db(audience_type)

        # Convert numbers to strings
        number_strings = [str(num) for num in user_data]

        # Join the number strings with commas
        numbers_csv = ', '.join(number_strings)
        
        # Test number line
        response = multiple_sms(numbers_csv, message)
        return admin_success(response)

# Send SMS to people
@app.route("/single_sms", methods=["POST"])
@admin_login_required
def single_sms():
    if request.method == 'POST':
        grade_level = request.form.get('grade-student')
        student_info = request.form.get('student_info')
        message = request.form.get('message')
        if not grade_level or not student_info:
            return admin_error("incomplete input provided!", 400)
        split_word = student_info.split()
        std_id = int(split_word[0])
        user_data = load_student_data_from_db(grade_level, std_id)
        mobile = user_data[11]
        student_name = user_data[1]
        date_today = date.today()
        message = f"Dear Guardian, records show that {student_name} is absent today {date_today} for unknown reason. Please call 9828113595 for details. - CJ_School"

        # Test number line
        response = SMS_sociair(mobile, message)
        return admin_success(response)
    else:
        return error("Unauthorized Access attempt", 400)


# Manage Settings
@app.route("/settings")
@admin_login_required
def manage_settings():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE admin_id = %s"
            cursor.execute(data_query, (session["admin_id"],))
            row = cursor.fetchone()
            connection.close()
        username = row[1]
        id = row[0]
        return render_template("settings.html", username = username, id = id)
    except Exception as e:
        return admin_error(e, 404)

# For Student Info UX
@app.route("/student-info")
@admin_login_required
def student_info():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE admin_id = %s"
            cursor.execute(data_query, (session["admin_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT * FROM grade_nursery")
            std_nursery = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_LKG")
            std_LKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_UKG")
            std_UKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_1")
            std_1 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_2")
            std_2 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_3")
            std_3 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_4")
            std_4 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_5")
            std_5 = cursor.fetchall()

            connection.close()
            template_data = {
                'username' : row[1],
                'std_nursery' : std_nursery,
                'std_LKG' : std_LKG,
                'std_UKG' : std_UKG,
                'std_1' : std_1,
                'std_2' : std_2,
                'std_3' : std_3,
                'std_4' : std_4,
                'std_5' : std_5,
                'selected_std' : None
            }
            return render_template("student-info.html", **template_data)
    except Exception as e:
        return admin_error(e, 404)


# For Staff Info UX
@app.route("/staff-info", methods = ['GET'])
@admin_login_required
def staff_info():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM admin WHERE admin_id = %s"
            cursor.execute(data_query, (session["admin_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT * FROM staff")
            staff_all = cursor.fetchall()

            connection.close()
            template_data = {
                'username' : row[1],
                'staff_all' : staff_all,
                'selected_staff' : None
            }
            return render_template("staff-info.html", **template_data)
    except Exception as e:
        return admin_error(e, 404)

######################## Staff Route #########################
@app.route("/staff")
@staff_login_required
def staff():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM staff WHERE staff_id = %s"
            cursor.execute(data_query, (session["staff_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT * FROM grade_nursery")
            std_nursery = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_LKG")
            std_LKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_UKG")
            std_UKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_1")
            std_1 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_2")
            std_2 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_3")
            std_3 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_4")
            std_4 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_5")
            std_5 = cursor.fetchall()

            connection.close()
            template_data = {
                'username' : row[1],
                'std_nursery' : std_nursery,
                'std_LKG' : std_LKG,
                'std_UKG' : std_UKG,
                'std_1' : std_1,
                'std_2' : std_2,
                'std_3' : std_3,
                'std_4' : std_4,
                'std_5' : std_5
            }
            return render_template("staff.html", **template_data)
    except Exception as e:
        return staff_error(e, 404)

# Student Attendance for Staff
@app.route("/attendance")
@staff_login_required
def attendance():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM staff WHERE staff_id = %s"
            cursor.execute(data_query, (session["staff_id"],))
            row = cursor.fetchone()

            cursor.execute("SELECT * FROM grade_nursery")
            std_nursery = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_LKG")
            std_LKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_UKG")
            std_UKG = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_1")
            std_1 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_2")
            std_2 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_3")
            std_3 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_4")
            std_4 = cursor.fetchall()

            cursor.execute("SELECT * FROM grade_5")
            std_5 = cursor.fetchall()

            connection.close()
            template_data = {
                'class_assigned' : row[10],
                'username' : row[1],
                'std_nursery' : std_nursery,
                'std_LKG' : std_LKG,
                'std_UKG' : std_UKG,
                'std_1' : std_1,
                'std_2' : std_2,
                'std_3' : std_3,
                'std_4' : std_4,
                'std_5' : std_5
            }
            return render_template("attendance.html", **template_data)
    except Exception as e:
        return staff_error(e, 404)

# Calendar
@app.route("/calendar")
def calendar():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM calendar_events"
            cursor.execute(data_query)
            events = cursor.fetchall()
            connection.close()
            event_list = []
            for event in events:
                if event[6] == None:
                    event_dict = {
                    'id': event[0],
                    'title': event[1],
                    'description': event[2],
                    'type': event[3],
                    'date': event[4],
                    'everyYear': event[5],
                    'color': event[7]
                }
                else:
                    event_dict = {
                        'id': event[0],
                        'title': event[1],
                        'description': event[2],
                        'type': event[3],
                        'date': convert_date(str(event[4])),
                        'end_date': convert_date(str(event[6])),
                        'everyYear': event[5],
                        'color': event[7]
                    }
                event_list.append(event_dict)
        return render_template("calendar.html", events = event_list)
    except:
        return render_template("calendar.html")

# Add event to calendar
@app.route("/add_event", methods = ["POST"])
@admin_login_required
def add_event():
    if request.method == "POST":
        event_title = request.form.get("event_title")
        description = request.form.get("description")
        event_type = request.form.get("event_type")
        event_date = request.form.get("event_date")
        end_date = request.form.get("end_date")
        everyYear = request.form.get("everyYear")
        if not event_title or not description or not event_type or not event_date or not everyYear:
            return admin_error("Incomplete form submitted!", 400)
        else:
            if event_type == "holiday":
                color = "#a50c30"
            elif event_type == "exam_schedule":
                color = "green"
            elif event_type == "extra_curricular":
                color = "blue"
            else:
                color = "#f77777"
            data = (event_title, description, event_type, event_date, everyYear, end_date, color)
            EventAdded = AddEventToCalendar(data)
            if EventAdded:
                return admin_success("Event Added Successfully")
            else:
                return admin_error("Error Adding Event!", 400)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/temp_image'
app.config['NOTICE_FOLDER'] = 'static/image_notice'
app.config['STAFF_PROFILE_FOLDER'] = 'static/staff-profile-temp'
app.config['INVESTORS_PROFILE_FOLDER'] = 'static/investors-profile-temp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/tnx_update", methods = ["POST"])
@member_login_required
def tnx_update():
    if request.method == "POST":
        deposited_by = request.form.get("deposited_by")
        amount = request.form.get("amount")
        date = request.form.get("date")
        file = request.files["file"]
        if not deposited_by or not amount or not date or not file:
            return error ("Incomplete form submitted!", 400)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            inv_id = session["member_id"]
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename))
            FilePath = BASE_DIR + f'/static/temp_image/{filename}'
            with open(FilePath, "rb") as File:
                BinaryData = File.read()
            image_format = imghdr.what(None, BinaryData)
            data = (inv_id, amount, deposited_by, date, BinaryData, image_format)
            IsInserted = InsertBlob(data)
            if IsInserted:
                return success("Transaction Uploaded Successfully")
        else:
            return error("Error occurred!", 400)     

# Add Notice
@app.route("/add_notice", methods = ["POST"])
@admin_login_required
def add_notice():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        file = request.files["file"]
        if not title or not content:
            return admin_error ("Required field cannot be empty!", 400)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            admin_id = session["admin_id"]
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['NOTICE_FOLDER'], filename))
            FilePath = f'\static\image_notice\{filename}'
            data = (title, content, FilePath)
            IsAdded = InsertNotice(data)
            if IsAdded:
                return admin_success("Notice Added Successfully")
        elif not file:
            data = (title, content, "")
            IsAdded = InsertNotice(data)
            if IsAdded:
                return admin_success("Notice Added Successfully")
        else:
            return admin_error("Error occurred!", 400)     

# Update investor profile
@app.route("/update-investor-profile", methods = ["POST"])
@member_login_required
def update_investor_profile():
    if request.method == "POST":
        id = request.form.get("id")
        file = request.files["file"]
        full_name = request.form.get("name")
        education = request.form.get("education")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        about_me = request.form.get("about_me")
        facebook_url = request.form.get("facebook_url")
        twitter_url = request.form.get("twitter_url")
        linkedin_url = request.form.get("linkedin_url")
        instagram_url = request.form.get("instagram_url")
        tiktok_url = request.form.get("tiktok_url")

        if not id or not full_name or not dob or not gender or not email or not phone or not address:
            return error("Your form seems to be Incomplete. Please recheck and submit again", 400)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            FilePath = BASE_DIR + f'/static/investors-profile-temp/{filename}'
            # Check if the file already exists
            if os.path.exists(FilePath):
                # Remove the existing file
                os.remove(FilePath)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['INVESTORS_PROFILE_FOLDER'], filename))
            with open(FilePath, "rb") as File:
                BinaryData = File.read()
            image_format = imghdr.what(None, BinaryData)

        data1 = (full_name, education, gender, dob, email, phone, address, about_me, BinaryData, image_format)
        data2 = (facebook_url, twitter_url, linkedin_url, instagram_url, tiktok_url)
        # update to DB
        is_updated = update_member_profile_into_db(id, data1, data2)
        if is_updated == True:
            return success("Profile updated successfully")
        else:
            return error("Could not update the data", 400)

# Update staff profile
@app.route("/update-staff-profile", methods = ["POST"])
@staff_login_required
def update_staff_profile():
    if request.method == "POST":
        id = request.form.get("id")
        file = request.files["file"]
        full_name = request.form.get("name")
        education = request.form.get("education")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        about_me = request.form.get("about_me")
        facebook_url = request.form.get("facebook_url")
        twitter_url = request.form.get("twitter_url")
        linkedin_url = request.form.get("linkedin_url")
        instagram_url = request.form.get("instagram_url")
        tiktok_url = request.form.get("tiktok_url")

        if not id or not full_name or not dob or not gender or not email or not phone or not address:
            return staff_error("Your form seems to be Incomplete. Please recheck and submit again", 400)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            FilePath = BASE_DIR + f'/static/staff-profile-temp/{filename}'
            # Check if the file already exists
            if os.path.exists(FilePath):
                # Remove the existing file
                os.remove(FilePath)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['STAFF_PROFILE_FOLDER'], filename))
            with open(FilePath, "rb") as File:
                BinaryData = File.read()
            image_format = imghdr.what(None, BinaryData)

        data1 = (full_name, education, gender, dob, email, phone, address, about_me, BinaryData, image_format)
        data2 = (facebook_url, twitter_url, linkedin_url, instagram_url, tiktok_url)
        # update to DB
        is_updated = update_staff_profile_into_db(id, data1, data2)
        if is_updated == True:
            return staff_success("Profile updated successfully")
        else:
            return staff_error("Could not update the data", 400)


@app.route("/change-pwd", methods = ["POST"])
@login_required
def change_pwd():
    if request.method == "POST":
        account_type = request.form.get("account_type")
        current_pwd = request.form.get("current_pwd")
        new_pwd = request.form.get("new_pwd")
        confirm_pwd = request.form.get("confirm_pwd")
        if not current_pwd or not new_pwd or not confirm_pwd:
            return error("Missing Form Data!", 404)

        # comparing New Pw and Confirm New Pw
        elif new_pwd != confirm_pwd:
            return error("Password and confirm password must be same.", 400)

        if account_type == 'investor':
            id = session["member_id"]
            data = (account_type, id)
            row = retrieve_user_hash(data)
            if check_password_hash(row[4], current_pwd):
                hash_pw = generate_password_hash(new_pwd)
                data = (hash_pw, id)
                if change_investor_pw(data):
                    return success("Password updated successfully.")
                else:
                    return error("Error updating password.", 500)
            else:
                return error("Please provide a valid current password", 400)
            
        elif account_type == 'staff':
            id = session["staff_id"]
            data = (account_type, id)
            row = retrieve_user_hash(data)
            if check_password_hash(row[4], current_pwd):
                hash_pw = generate_password_hash(new_pwd)
                data = (hash_pw, id)
                if change_staff_pw(data):
                    return staff_success("Password updated successfully.")
                else:
                    return staff_error("Error updating password.", 500)
            else:
                return staff_error("Please provide a valid current password", 400)

        elif account_type == 'std_id':
            id = session['std_id']

        else:
            id = session["admin_id"]
            data = (account_type, id)
            row = retrieve_user_hash(data)
            if check_password_hash(row[4], current_pwd):
                hash_pw = generate_password_hash(new_pwd)
                data = (hash_pw, id)
                if change_admin_pw(data):
                    return admin_success("Password updated successfully.")
                else:
                    return admin_error("Error updating password.", 500)
            else:
                return admin_error("Please provide a valid current password", 400)

# Register user User
@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/register-member", methods=["GET", "POST"])
def register_member():
    session.clear()
    """Register member"""
    if request.method == "POST":
        name = request.form.get("full_name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        pwd = request.form.get("password")
        confirm_pwd = request.form.get("confirm_pwd")
        access_key = request.form.get("access_key")

        if not name or not email or not mobile or not pwd or not confirm_pwd or not access_key:
            return error("Form data missiong. Please check and submit again!", 400)
        
        # comparing password and confirm password
        elif pwd != confirm_pwd:
            return error("Password and confirm password missmatch.", 400)

        # Check if registration key is valid
        account_type = 'member'
        data = (access_key, account_type)
        if not check_access_key(data):
            return error("Please provide a valid Registration Key.", 400)
        if not destroyOTP(access_key):
            return error("Error in validating Key. Please contact administrator for help.")
        
        #Check if account already exist
        data = (email, mobile)
        if investor_account_exist(data):
            return error("User Email/Mobile already exists", 400)

        # if everything goes well:
        hash_pw = generate_password_hash(pwd)

        if account_type == "member":
            data = (name, email, mobile, hash_pw)
            is_registered = insert_director_into_db(data)
            if is_registered == True:
                return success("You have successfully registered!")
            else:
                return error("Error in creating account", 400)
    else:
        return render_template("register.html")

@app.route("/register-staff", methods=["GET", "POST"])
def register_staff():
    session.clear()
    """Register member"""
    if request.method == "POST":
        name = request.form.get("full_name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        pwd = request.form.get("password")
        confirm_pwd = request.form.get("confirm_pwd")
        access_key = request.form.get("access_key")

        if not name or not email or not mobile or not pwd or not confirm_pwd or not access_key:
            return error("Form data missiong. Please check and submit again!", 400)
        
        # comparing password and confirm password
        elif pwd != confirm_pwd:
            return error("Password and confirm password missmatch.", 400)

        # Check if registration key is valid
        account_type = 'staff'
        data = (access_key, account_type)
        if not check_access_key(data):
            return error("Please provide a valid Registration Key.", 400)
        if not destroyOTP(access_key):
            return error("Error in validating Key. Please contact administrator for help.")
        
        #Check if account already exist
        data = (email, mobile)
        if staff_account_exist_in_db(data):
            return error("User Email/Mobile already exists", 400)

        # if everything goes well:
        hash_pw = generate_password_hash(pwd)

        if account_type == "staff":
            data = (name, email, mobile, hash_pw)
            is_registered = insert_staff_into_db(data)
            if is_registered == True:
                return success("You have successfully registered!")
            else:
                return error("Error in creating account", 400)
    else:
        return render_template("register.html")


# Admit Student to DB
@app.route("/admit_student", methods = ["GET", "POST"])
@admin_login_required
def admit_student():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        full_name_nepali = request.form.get("full_name_nepali")
        dob = request.form.get("dob")
        grade = request.form.get("grade")
        gender = request.form.get("gender")
        father_name = request.form.get("father_name")
        father_mobile = request.form.get("father_mobile")
        mother_name = request.form.get("mother_name")
        mother_mobile = request.form.get("mother_mobile")
        p_address = request.form.get("p_address")
        guardian_name = request.form.get("guardian_name")
        guardian_mobile = request.form.get("guardian_mobile")
        guardian_relation = request.form.get("guardian_relation")

        if not full_name or not full_name_nepali or not dob or not grade or not father_name or not mother_name or not p_address or not guardian_name or not guardian_mobile or not guardian_relation:
            return admin_error("Your form seems to be Incomplete. Please recheck your form and submit AGAIN", 400)
        
        data = (full_name, full_name_nepali, dob, gender, father_name, father_mobile, mother_name, mother_mobile, p_address, guardian_name, guardian_mobile, guardian_relation)
        is_registered = admit_student_into_db(grade, data)

        if is_registered == True:
            message = f"Hi {guardian_name}, Your admission process for {grade} has been confirmed! Thank you for choosing our school for your child's early childhood education needs. - Chandrajyoti School"
            SMS_sociair(guardian_mobile, message)
            return admin_success("Form data submitted successfully")
        else:
            return admin_error("Could not update to database", 400)
    else:
        return render_template("admit-student.html")

# Open Pre-registration for Admission
@app.route("/admission-form", methods = ["GET", "POST"])
@member_login_required
def admission():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        dob = request.form.get("dob")
        grade = request.form.get("grade")
        gender = request.form.get("gender")
        father_name = request.form.get("father_name")
        father_mobile = request.form.get("father_mobile")
        mother_name = request.form.get("mother_name")
        mother_mobile = request.form.get("mother_mobile")
        p_address = request.form.get("p_address")
        guardian_name = request.form.get("guardian_name")
        guardian_mobile = request.form.get("guardian_mobile")
        guardian_relation = request.form.get("guardian_relation")
        full_name_nepali = request.form.get("full_name_nepali")

        if not full_name or not dob or not grade or not father_name or not mother_name or not p_address or not guardian_name or not guardian_mobile or not guardian_relation or not full_name_nepali:
            return error("Your form seems to be Incomplete. Please recheck your form and submit AGAIN", 400)
        
        data = (full_name, dob, grade, gender, father_name, father_mobile, mother_name, mother_mobile, p_address, guardian_name, guardian_mobile, guardian_relation, full_name_nepali)
        is_registered = pre_register_student(data)

        if is_registered == True:
            message = f"Hi {guardian_name}, Your admission process for {grade} has been confirmed! Thank you for choosing our school for your child's early childhood education needs. - Chandrajyoti School"
            SMS_sociair(guardian_mobile, message)
            return success("Pre-registration successfull")
        else:
            return error("Error on form submission.", 400)
    else:
        return render_template("admission-form.html")


@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms-and-conditions.html")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

# forgot email
@app.route("/forgot-username", methods = ["GET", "POST"])
def forgot_username():
    if request.method == "POST":
        return error("This feature is not available. We will include it in future update", "and Apology")
    else:
        return render_template("forgot-username.html")

# Reset Pw
@app.route("/forgot-password", methods = ["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        mobile = request.form.get("mobile")
        if not mobile:
            return error("Missing mobile number")
        return error("For the security reasons the feature you tried to access is not currently not available. Contact IT administrator for help.", ": Feature not available!")
    else:
        return render_template("forgot-password.html")


@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/our-teams")
def our_teams():
    return render_template("team-chandrajyoti.html")

@app.route("/careers")
def careers():
    jobs = load_jobs_from_db()
    return render_template("careers.html", jobs = jobs)

@app.route("/careers/<id>")
def career_detail(id):
    job = load_job_from_db(id)
    is_expired = error(has_expired(job["deadline"]), 400)
    return render_template("career-detail.html", job = job, is_expired = is_expired)

# News and updates
@app.route("/newsandupdates")
def newsandupdates():
    notices = load_notices_from_db()
    return render_template("notice.html", notices = notices)

@app.route("/newsandupdates/<id>")
def notice_detail(id):
    notice = load_notice_from_db(id)
    return render_template("notice-details.html", notice = notice)
    
# Create Token
@app.route("/create_token", methods = ["POST"])
@admin_login_required
def create_token():
    if request.method == "POST":
        access_type = request.form.get("account_type")
        if request.form.get("mobile"):
            phone_number = int(request.form.get("mobile"))
        if not access_type:
            return admin_error("Registraton type not selected!", 400)
        new_token = secrets.token_hex(3)
        data = (new_token, phone_number, access_type)
        IsInserted = access_key_into_db(data)
        # SMS CREATED TOKEN TO THE RECIPIENT
        if IsInserted == True:
            message = f"Welcome to Chandrajyoti School Family! Your access code for {access_type} account is: {new_token}. Do not share it with anyone."
            response_msg = SMS_sociair(phone_number, message)
            return admin_success(response_msg)
        # check if user exists
    else:
        return render_template("create-token.html")

@app.route("/profile")
@member_login_required
def profile():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            # fetch data of logged in User
            data_query = "SELECT * FROM investors_profile WHERE id = %s"
            cursor.execute(data_query, (session["member_id"],))
            row = cursor.fetchone()

            data_query = "SELECT * FROM investors_social_media WHERE id = %s"
            cursor.execute(data_query, (session["member_id"],))
            social_media = cursor.fetchone()

            connection.close()
            # retrieve Image from DB
            if row[11]:
                id = str(row[0])
                image_data = row[11]
                image_format = row[12]
                retrieve_investor_photo_from_db (id, image_data, image_format)
        template_data = {
            'username' : row[2],
            'profile' : row,
            'social_media' : social_media
        }
        return render_template("profile.html", **template_data)
    except Exception as e:
        return error(e, 400)

# Staff profile view
@app.route("/staff-profile")
@staff_login_required
def staff_profile():
    try:
        connection = mysql.connect (
            host = "23.106.53.56",
            user = "chakmake_cjadmin",
            password = "Maheshraj##123",
            database = "chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            # fetch data of logged in User
            data_query = "SELECT * FROM staff_profile WHERE id = %s"
            cursor.execute(data_query, (session["staff_id"],))
            row = cursor.fetchone()

            data_query = "SELECT * FROM staff_social_media WHERE id = %s"
            cursor.execute(data_query, (session["staff_id"],))
            social_media = cursor.fetchone()

            connection.close()
            # retrieve Image from DB
            id = str(row[0])
            image_data = row[11]
            image_format = row[12]
            retrieve_staff_photo_from_db (id, image_data, image_format)
        template_data = {
            'username' : row[2],
            'profile' : row,
            'social_media' : social_media
        }
        return render_template("profile-staff.html", **template_data)
    except Exception as e:
        return error(e, 400)