from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from dotenv import load_dotenv
import os
import secrets
from flask_session import Session
from dbmodule import insert_student_into_db, check_access_key, investor_account_exist, insert_director_into_db, access_key_into_db, transaction_info_into_db, destroyOTP
from database import load_job_from_db, load_jobs_from_db
from memberdb import change_investor_pw, change_admin_pw
from userdb import staff_account_exist, member_account_exist, student_account_exist, admin_account_exist, retrieve_user_data, retrieve_user_hash
from helpers import error, success, login_required, number_validity, SMS_sociair, has_expired, npr, TrunDecimal
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
import mysql.connector as mysql
from werkzeug.utils import secure_filename
import urllib.request
from blobdb import InsertBlob, retrieve_image_from_db
import imghdr

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
    try:
        connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
        )
        with connection.cursor() as cursor:
            data_query = "SELECT * FROM investors WHERE inv_id = %s"
            cursor.execute(data_query, (session["member_id"],))
            row = cursor.fetchone()
            connection.close()
            return render_template("index.html", username = row[1])
    except:
        try:
            connection = mysql.connect (
            host="23.106.53.56",
            user="chakmake_cjadmin",
            password ="Maheshraj##123",
            database="chakmake_cjschool"
            )
            with connection.cursor() as cursor:
                data_query = "SELECT * FROM staff WHERE staff_id = %s"
                cursor.execute(data_query, (session["staff_id"],))
                row = cursor.fetchone()
                connection.close()
                return render_template("index.html", username = row[1])
        except:
            try:
                connection = mysql.connect (
                    host = "23.106.53.56",
                    user = "chakmake_cjadmin",
                    password = "Maheshraj##123",
                    database = "chakmake_cjschool"
                )
                with connection.cursor() as cursor:
                    data_query = "SELECT * FROM student WHERE std_id = %s"
                    cursor.execute(data_query, (session["std_id"],))
                    row = cursor.fetchone()
                    connection.close()
                    return render_template("index.html", username = row[1])
            except:
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
                return error("Database Issue", 1011)

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
                    return redirect("/dashboard")
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

@app.route("/dashboard")
@login_required
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

            cursor.execute("SELECT count(*) FROM student")
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


# Admin Dashboard
@app.route("/admin")
@login_required
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

            cursor.execute("SELECT count(*) FROM student")
            std_count = cursor.fetchone()

            connection.close()
            template_data = {
                'username' : row[1],
                'inv_count' : inv_count[0],
                'staff_count' : staff_count[0],
                'std_count' : std_count[0]
            }
            return render_template("admin.html", **template_data)
    except Exception as e:
        return error(e, 404)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/temp_image'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/tnx_update", methods = ["POST"])
@login_required
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
            FilePath = (os.path.join(os.path.abspath(os.path.dirname(__file__)), f'static\\temp_image\{filename}'))
            with open(FilePath, "rb") as File:
                BinaryData = File.read()
            image_format = imghdr.what(None, BinaryData)
            data = (inv_id, amount, deposited_by, date, BinaryData, image_format)
            IsInserted = InsertBlob(data)
            if IsInserted:
                return success("Transaction Uploaded Successfully")
        else:
            return error("Error occurred!", 400)     
        
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
                    return success("Password updated successfully.")
                else:
                    return error("Error updating password.", 500)
            else:
                return error("Please provide a valid current password", 400)

# Register user as Director
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """Register user"""
    if request.method == "POST":
        # account_type = request.form.get("account_type")
        account_type = "investor"
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
        data = (access_key, account_type)
        if not check_access_key(data):
            return error("Please provide a valid Registration Key.", 400)
        destroyOTP(access_key)
        
        #Check if account already exist
        data = (email, mobile)
        if investor_account_exist(data):
            return error(" account already exist.", 400)

        # if everything goes well:
        hash_pw = generate_password_hash(pwd)

        if account_type == "investor":
            data = (name, email, mobile, hash_pw)
            is_registered = insert_director_into_db(data)
            if is_registered == True:
                return success("You have successfully registered!")
            else:
                return error(is_registered, 400)
    else:
        return render_template("register.html")


@app.route("/admission-form", methods = ["GET", "POST"])
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
        is_registered = insert_student_into_db(data)

        if is_registered == True:
            return success("Form data submitted successfully")
        else:
            return error("Could not update to database", 400)
    else:
        return render_template("admission-form.html")

@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms-and-conditions.html")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route("/forgot-username", methods = ["GET", "POST"])
def forgot_username():
    if request.method == "POST":
        return error("This feature is not available. We will include it in future update", "and Apology")
    else:
        return render_template("forgot-username.html")


@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/our-teams")
@login_required
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
    
# Create Token
@app.route("/create_token", methods = ["POST"])
@login_required
def create_token():
    if request.method == "POST":
        access_type = request.form.get("account_type")
        if request.form.get("mobile"):
            phone_number = int(request.form.get("mobile"))
        if not access_type:
            return error("Registraton type not selected!", 400)
        new_token = secrets.token_hex(3)
        data = (new_token, access_type)
        IsInserted = access_key_into_db(data)
        # SMS CREATED TOKEN TO THE RECIPIENT
        if IsInserted == True:
            message = f"Welcome to Chandrajyoti School Family! Your access code for {access_type} account is: {new_token}. Do not share it with anyone."
            response_msg = SMS_sociair(phone_number, message)
            return success(response_msg)
        # check if user exists
    else:
        return render_template("create-token.html")

@app.route("/profile")
@login_required
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
            data_query = "SELECT * FROM investors WHERE inv_id = %s"
            cursor.execute(data_query, (session["member_id"],))
            row = cursor.fetchone()
            template_data = {
                'username' : row[1],
                'profile' : row
             }
            return render_template("profile.html", **template_data)
    except:
        return "1009: Error occurred during database connection"