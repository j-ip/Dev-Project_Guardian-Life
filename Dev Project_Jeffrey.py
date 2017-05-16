#Jeffrey Ip - Dev Project
"""
Spyder Editor
Openweathermap test link: api.openweathermap.org/data/2.5/weather?zip=11209,us&units=imperial&APPID=d9e898fca08f300c113b57b85dad2c41
"""
import json
import urllib2
import sys
from datetime import date
#creates a weather class
class weather:
    apiurl = "http://api.openweathermap.org/data/2.5/weather?units=imperial" #apiurl builder
    apiforecasturl = "http://api.openweathermap.org/data/2.5/forecast?units=imperial"
    country = ""
    zipcode = ""
    current_temp = 0
    max_temp = 0
    min_temp = 0
    wind_speed = 0
    desc = ""
    location = ""
    __key = "" #private user key
    __data = {} #contains all weather data for the weather class
    __forecastdata = {} #contains all weather data for the weather class
    
    def __init__(self, zipcode, key = "d9e898fca08f300c113b57b85dad2c41"): #class constructor
        self.apiurl = self.apiurl + "&zip=" + str(zipcode) + "&APPID=" + key #apiurl string builder
        self.apiforecasturl = self.apiforecasturl + "&zip=" + str(zipcode) + "&APPID=" + key #apiurl string builder
        self.key = key
        self.data = json.load(urllib2.urlopen(self.apiurl))
        self.forecastdata = json.load(urllib2.urlopen(self.apiforecasturl))
        self.country = self.data['sys']['country']
        self.zipcode = zipcode
        self.current_temp = self.data['main']['temp']
        self.max_temp = self.data['main']['temp_max']
        self.min_temp = self.data['main']['temp_min']
        self.wind_speed = self.data['wind']['speed']
        self.desc = self.data['weather'][0]['description']
        self.location = self.data['name']
        
    def showSummary(self): #prints a full summary of the current weather object
        print ('\nToday\'s weather in %s is %s.\nThe current temperature is %s degrees fahrenheit with a high of %s degrees and a low of %s degrees with wind speeds up to %smph.\n ') % (self.location, self.desc, self.current_temp, self.max_temp, self.min_temp, self.wind_speed)
    
    def getTemp(self, minmax): #return temperature based off parameters; default: current
        if minmax == "min":
            return self.min_temp
        elif minmax == "max":
            return self.max_temp
        else:
            return self.current_temp
    
    def getWindSpeed(self): #return wind speed
        return self.wind_speed
    """
    def getForecast(self):
        accuracy = False
        for i in self.forecastdata['list']:
            d = i['dt_txt'].split(" ")
            if d[0] == str(date.today()):
                print (i['main']['temp'])
                accuracy = True
        if accuracy == False:
            for i in self.forecastdata['list']:
                d = i['dt_txt'].split(" ")
                if d[0] == str(date.today() + timedelta(1)):
                    print (i['main']['temp'])
                    accuracy = True
        return 0
    """
    
    def getForecast(self): #print 5 day 3 hour forecast
        baseDay = self.forecastdata['list'][0]['dt_txt'].split(" ")[0] #formatting purposes: saves the first day
        print ('\nDate: %s') % (baseDay)
        for i in self.forecastdata['list']:
            high = i['main']['temp_max']
            low = i['main']['temp_min']
            hourly = i['dt_txt'].split(" ")
            if hourly[0] == baseDay: #if base day is already printed, do not reprint (works only when sorted)
                print ('   Time: %s    ' + 'High: %.2f' + '   Low: %.2f') % (hourly[1], high, low) #includes decimal formatting for visual purposes
            else:
                print ('Date: %s') % (hourly[0]) #print date if it is a new day (works only when sorted)
                print ('   Time: %s    High: %.2f   Low: %.2f') % (hourly[1], high, low)
                baseDay = hourly[0]
        print ('\n')
        return 0
    
def showMenu(zipcode): #method to display the menu taking in zipcode as a parameter
    thisWeather = weather(zipcode) #creating a weather object
    while True:
        print ("***************Weather API Console Program Menu***************")
        print ("************All temperatures are shown in fahrenheit**********")
        print ("1. Show full weather summary")
        print ("2. Show today's temperature (highs and lows)")
        print ("3. Show windspeed")
        print ("4. Show 5 day 3 hour forecast")
        print ("5. Change zipcode")
        print ("All other inputs to exit the program")
        user_selection = str(raw_input("Please select from the above menu items: ")) #user selection input
        if user_selection == "1":
            thisWeather.showSummary()
        elif user_selection == "2":
            print ("\nToday's temperature in %s is %s with a high of %s and a low of %s.\n") % (thisWeather.location, thisWeather.getTemp("current"), thisWeather.getTemp("max"), thisWeather.getTemp("min"))
        elif user_selection == "3":
            print ("\nThe wind speed in %s is %smph.\n") % (thisWeather.location, thisWeather.getWindSpeed())
        elif user_selection == "4":
            thisWeather.getForecast()
        elif user_selection == "5": #recreates thisWeather object with a new user inputted zipcode
            userInput()
            break
        else:
            print ("Terminating program...")
            return 0
def userInput(): #user input for zipcode and HTTPError check
    try:
        user_zip = str(raw_input("Please enter a valid zipcode to display the menu items or x to exit: "))
        if user_zip == "x":
            try:
                sys.exit(0)
            except:
                print ("Terminating program...")
                return 0
        print ("\n")
        showMenu(user_zip)
    except urllib2.HTTPError:
        print("The zipcode entered is invalid.")
        userInput() #if API returns an error, restart userInput
    return 0

userInput() #begin the program