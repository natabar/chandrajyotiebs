from flask import redirect, render_template, request, session
from functools import wraps
from nepali_phone_number import NepaliPhoneNumber
import requests, math
from datetime import date, datetime

sociair_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiOTdhMGI4Y2MyMjlkYjg0ZDQ0NGYwMTdlNjFhYmM3ZTMxZmI2YzlkZGI0ZTlhNGRmNjQ0M2IzOTUzNmI3NmQyOWQxNGE4M2Q2ZjkxNWJjODEiLCJpYXQiOjE2ODM1NzQ0NjYuNDg5NjM4LCJuYmYiOjE2ODM1NzQ0NjYuNDg5NjQ0LCJleHAiOjE3MTUxOTY4NjYuNDcxMTQ0LCJzdWIiOiIxMDY4Iiwic2NvcGVzIjpbXX0.cGROAmZUbpbeNN4dKsVVe5IEWBRzLupnVjR3j6gMRMrEfKEX3vfe6wxKDexhLhafU4MAp5rr42ikyH9lMfXZcMNzoMxNmRyAcJkqLsbyAWK9lEaEo9cBRnQJZZ7QBu28EnH134Jy3VzM2hbmupj9vVShk1juZeSdSJnyHKrc7zUpeu4nCO738Q2e4HA1Engc2-erpdJ8ZYYIkPnJYf5eLM09MZgY6nswbOzQgLcDNhtQ3NH6eySLTBYmQiIWJJ9StAUJl4rY1Y1ivGEiRUSSZZfS4O4nOsnBYHhes1SHPO6Btyhl91h4DZ3tKWJ2B7p8mj4WHl366aJ7MEHI31WKaVA8gfh4v4tkgpHWrSLfTnaYhWerfvmgd54z7DskMMpvqixFQ3wo81lmcjFkDbiWaGz4YL5UIB-9O1DegSX4zhmP5hfWdftjpAeFHfkeuR8rHTtlgTnAhzkxlpR_-liWQAPDZWbYoZROUfBZCRjXeNE2OCYhualFwKrmchCSf4GG5-Mh03TE35lGBeZZGipyVuIDD15wq8uo4bR0EJOQCgB6RrzxNSj4Rm6M4n8QzMXschysCXyNqqanSRgcWJXjgnUqlyhEDrogad_cLRL0ClVBiLS6sf2aSOBIuey8RBOdrqQOpbyk-OU2DTuZPwVqRdxssKF6v7mr65b3GCMGn7s'

def error(message, code):
    return render_template("error.html", message = message, code = code)

def admin_error(message, code):
    return render_template("error-admin.html", message = message, code = code)

def staff_error(message, code):
    return render_template("error-staff.html", message = message, code = code)

def success(message):
    return render_template("success.html", message = message)

def admin_success(message):
    return render_template("success-admin.html", message = message)

def staff_success(message):
    return render_template("success-staff.html", message = message)

def number_validity(number):
    phone_number = NepaliPhoneNumber(english_number_input = number)
    carrier = phone_number.get_number_detail()["network_provider"]
    return (phone_number.is_valid_number(), carrier)

def CheckSMS_Bal(carrier, message):
    try:
        headers = {
            "Authorization": sociair_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        request_url = 'https://sms.sociair.com/api/balance'
        response = requests.get(request_url, headers = headers)
        response_msg = response.json()
        code = response.status_code
        if code == 200:
            msg_len = len(message)
            msg_num = math.ceil(msg_len/160)
            if response_msg["balance"] > msg_num * response_msg[carrier]:
                return True
            else:
                return False
        else:
            return (code, response_msg)
    except:
        return (503, "SMS service unavailable")

# Check SMS system Balance
def check_sms_system_bal():
    try:
        headers = {
            "Authorization": sociair_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        request_url = 'https://sms.sociair.com/api/balance'
        response = requests.get(request_url, headers = headers)
        response_msg = response.json()
        code = response.status_code
        if code == 200:
            return  response_msg["balance"]
        else:
            return False
    except:
        return (503, "SMS service unavailable")

def SMS_sociair(mobile, message):
    try:
        ValidityResponse = number_validity(mobile)
        carrier = f"{ValidityResponse[1].lower()}_rate"
        IsEnoughBal = CheckSMS_Bal(carrier, message)
        if IsEnoughBal:
            url = 'https://sms.sociair.com/api/sms'

            # Data to send in the request
            payload = {
                "message": message,
                "mobile": mobile
            }

            headers = {
                    "Authorization": sociair_token,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            # Post request to SMS API
            response = requests.post(url, json=payload, headers=headers)

            # check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()  # get the response data as a JSON object
                return data["message"]
            else:
                return "Error: failed to get data"
        else:
            return "Insufficient Balance. Please contact your SMS service provider"
    except:
        return "Error: SMS service failed"

def multiple_sms(list_mobile, message):
    try:
        url = 'https://sms.sociair.com/api/sms'
        # Data to send in the request
        payload = {
                "message": message,
                "mobile": list_mobile
            }
        headers = {
            "Authorization": sociair_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # Post request to SMS API
        response = requests.post(url, json=payload, headers=headers)

        # check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # get the response data as a JSON object
            return data["message"]
        else:
            data = response.json()
            return data
    except:
        return "Error: SMS service failed"

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("member_id") is None and session.get("admin_id") is None and session.get("staff_id") is None and session.get("std_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def member_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("member_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def staff_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("staff_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def student_login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("std_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def has_expired(date):
    return date < date.today()

def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%B %d, %Y')
    return formatted_date

def npr(value):
    """Format Values for Nepalese Rupees."""
    return f"Rs.{value:,.2f}"

def TrunDecimal(value):
    """Format Values for Nepalese Rupees."""
    return f"{value:,.2f}"