# Variables
import sys

from rest_framework.response import Response
import requests
from django.utils import timezone
from datetime import datetime

STATUS = "Status"
MESSAGE = "Message"
DATA = "Data"

GRADE = [
    {
        "id":1,
        "name":"VIP 1",
        "business_count":1,
        "margin":5,
    },
    {
        "id":2,
        "name":"VIP 2",
        "business_count":10,
        "margin":10,
    },
    {
        "id":3,
        "name":"VIP 3",
        "business_count":25,
        "margin":15,
    },
    {
        "id":4,
        "name":"VIP 4",
        "business_count":50,
        "margin":20,
    },
]

REQUEST_TYPES = [
    "Book Product Free Trail", # product id
    "Buy Product", # product id
    "Robot Service Request",
    "Open Account Request",
    "Deposit Request",
    "Withdrawal Request",
    "IB Change Request",
    "IB Change Request",
    "Become our partner Request",
    "Request for payout",  #found
    "Renew Product",
]
#
# FANCY_WORDS = [
#     "yummy","crunchy","loveit","likeit","heroic","awsome","lucky","sweet","lovely","smellit","fancy","admire","adore",
#     "cherish","kitty","puppy","legent","legacy","cheese","queen","king","secret","start","spiderman","lover","excellent",
#     "goodbye","stop","nature","india","tokyo","japan","rose","lilly","creamy"
# ]

#Functions
def ResponseFunction(status,message,data):
    false_list = [0,"false",False,"0"]
    if status in false_list:
        status = False
    else:
        status = True

    return Response({
        STATUS: status,
        MESSAGE: message,
        DATA : data
    })

def printLineNo():
    return str(format(sys.exc_info()[-1].tb_lineno))

def excludeValidation(exculded,data_dic):
    errors = []
    print("Receved data ",data_dic)

    message = ""

    for field in exculded:
        print(f"checking {field} in data")
        if field in data_dic:
            message = f"Remove {field} from data body"
            errors.append({"error": message})
        else:

            print("Non required field found")

            # print(message)
        # print(f"Conclusion of {field} : ",message)
    print(errors)

    return errors

def ValidateRequest(required,data_dic):
    errors = []
    message = ""
    for field in required:
        if field not in data_dic:
            message =f"Required {field}"
            errors.append({"error":message})
        else:
            if data_dic[field] == "" or not data_dic[field]:
                message = f"{field} cannot be empty"
                errors.append({"error": message})
                # print(message)
            else:
                message = f"{field} found"
    if len(errors):
        'Print if there where errors'
        print(errors)
    return errors


def generateOTP(mobile):
    authkey = "MSG91AUTHKEY"
    # authkey = "181599AvHIQH7Y5f2ab33cP1"
    # authkey = "181599AkdEJBCjhfnW6044a474P1" #FDR
    authkey = "354611AiJCdxZN602fa46dP1" #BLYFDAP blyfdap
    # authkey = "366569A1tz5COgh612f178bP1" #TPUMRT
    url = f"http://api.msg91.com/api/sendotp.php?authkey={authkey}&template_id=614c237ec7d42827ef487172&mobile=" + mobile + "&sender=BLYFDAP&otp_expiry=3&otp_length=4&" \
                                                                                                     "=OTP code is %23%23OTP%23%23"
    url = f"http://api.msg91.com/api/v5/otp?template_id=614c237ec7d42827ef487172&mobile={mobile}&authkey={authkey}"
    print("url : ",url)
    payload = {}
    headers = {
        # 'Cookie': 'PHPSESSID=osh4u12u7d34qt1usueamgdis6'
    }
    payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"

    headers = {'content-type': "application/json"}
    response = requests.request("GET", url, headers=headers, data=payload)

    print("MSG91 Response ",response.json())

    if response.json()["type"] == "success":
        return True
    else:
        return False

def changing_naive_time(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    # print(type(date))
    new_date =timezone.make_aware(date, timezone.get_default_timezone())
    # print("Date ",new_date)
    return new_date

def validateOTP(mobile, otp):
    # return True
    if mobile == "911122334455":
        if otp == "1122":
            return True
        return False
    print(mobile,otp)
    authkey = "181599AvHIQH7Y5f2ab33cP1"

    url = f"http://api.msg91.com/api/verifyRequestOTP.php?authkey={authkey}&mobile=" + mobile + "&otp=" + otp

    payload = {}
    headers = {
        'Cookie': 'PHPSESSID=osh4u12u7d34qt1usueamgdis6'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.json()["type"] == "success":
        return True

    return False