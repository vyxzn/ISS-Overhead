import requests
from datetime import datetime
import smtplib
import time

email = "[YOUR EMAIL HERE]"
password = "[EMAIL APP-PASSWORD HERE]"

MY_LAT = [YOUR LATITUDE]
MY_LONG = [YOUR LONGITUDE]

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
print(time_now)
def iss_over_me():
    return (MY_LAT + 5 >= iss_latitude >= MY_LAT -5) and (MY_LONG + 5 >= iss_latitude >= MY_LONG -5)

def is_dark():
    return time_now.hour >= sunset or time_now.hour <= sunrise

while True:
    if iss_over_me() and is_dark():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(email, password)
            connection.sendmail(from_addr=email, to_addrs=email, msg="Subject:Look Up\n\nThe ISS is right above you")
    time.sleep(60)
