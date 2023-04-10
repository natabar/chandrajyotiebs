from flask import redirect, render_template, request, session
from functools import wraps
from nepali_phone_number import NepaliPhoneNumber
import requests, math

sociair_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiOWIzY2Y4YzI0NWQyNWFhY2I0YTVjNDBjNDY4ZjIxMDcwMmFmZjk1NWNhMzJmYmU2MmZlY2M1MmUzNzc3ZjA4YjU2NzM5NTc0MmVkZWE5YWMiLCJpYXQiOjE2NjEyNzY4NDguNjk3Njg3LCJuYmYiOjE2NjEyNzY4NDguNjk3NjkxLCJleHAiOjE2OTI4MTI4NDguNjkzMzc0LCJzdWIiOiIzNDUiLCJzY29wZXMiOltdfQ.aBCgOYiLvd2BLHyK5Tb19O5S0lxdeqOZvN3GNqoUe2KoG375EyEP_6g0C29qBPBDo2DRy2S2MU5Qqx4JhF_qbg'

def error(message, code):
    return render_template("error.html", message=message, code=code)

def success(message):
    return render_template("success.html", message=message)

def number_validity(number):
    phone_number = NepaliPhoneNumber(english_number_input=number)
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

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None and session.get("emp_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def npr(value):
    """Format Values for Nepalese Rupees."""
    return f"Rs.{value:,.2f}"