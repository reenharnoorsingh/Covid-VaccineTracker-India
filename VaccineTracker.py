# Vaccine Tracker for India

# imports
import requests
from pygame import mixer
from datetime import datetime, timedelta
import time

# Insert search parameters here
age = int(input("Enter your age: "))  # input age
pincodes = [input("Enter the pincode: ")]  # input pincode
num_days = 6  # total slots searched
dose = input("Enter the dose number: ")  # number of dose
polling_interval = 1

print_flag = 'Y'

print("Starting the search for Covid Vaccine slots!")

actual = datetime.today()  # searches for the current day
list_format = [actual + timedelta(days=i)for i in range(num_days)]  # formats to a list
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

num_searches = 0
while True:
    counter = 0
    for pincode in pincodes:
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, given_date)  # api
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if(print_flag.lower() == 'y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session[f"available_capacity_dose{dose}"] > 0):
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Age: ", session["min_age_limit"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ",
                                          session["available_capacity"])
                                    print("\t Dose: ", dose)

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ",
                                              session["vaccine"])
                                    print("\n")
                                    counter = counter + 1
            else:
                print("No Response!")

    if counter == 0:
        print("No Vaccination slot available!, Search number:", num_searches)
        num_searches += 1
    else:
        mixer.init()
        mixer.music.load('sounds/dingdong.wav')
        mixer.music.play()
        print("Search Completed! Slots available")
        print("Book your slot at https://selfregistration.cowin.gov.in/ ")

    dt = datetime.now() + timedelta(minutes=polling_interval)

    while datetime.now() < dt:
        time.sleep(1)
