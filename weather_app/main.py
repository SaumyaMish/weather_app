from tkinter import *
from geopy.geocoders import Nominatim
from  timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk

# import geolocator_method
# from geolocator_method import *

#-------------------------------UI Design-------------------------------------------#
#
#
#           temp desc
#           cloud_cover
#           rain
#
#
#-------------------------------UI Design-------------------------------------------#

window = Tk()
window.title("Weather App")

# Also sets the (x,y) coordinates from the main screen of your device
window.geometry("900x550+300+100")
window.resizable(False,False)

# --------------------- Canvas images---------------------------------#
canvas = Canvas(width=700,height=500,bg="#FFFFFF",borderwidth=0,highlightthickness=0)

search_img = PhotoImage(file="images/search_bar.png")
canvas.create_image(250,50,image= search_img)


cloud_img = PhotoImage(file="images/cloud.png")
canvas.create_image(400,250,image=cloud_img)

blue_img = PhotoImage(file="images/blue_line.png")
canvas.create_image(450,450,image=blue_img)

canvas.pack(expand=True,fill=BOTH)

# ----------------------------Fixed Labels-------------------------------------#

current_wdr = Label(text="Current Weather",font=("arial",20,"bold"),background="#FFFFFF",foreground="black")
current_wdr.place(x=70,y=100)

#description labels

humidity = Label(text="Humidity",font=("arial",14,"bold"),background="#00A1C9",foreground="#FFFFFF")
humidity.place(x=200,y=420)

cloud_cover_val = Label(text="Cloudy",font=("arial",14,"bold"),background="#00A1C9",foreground="#FFFFFF")
cloud_cover_val.place(x=350,y=420)

wind = Label(text="Wind Speed",font=("arial",14,"bold"),background="#00A1C9",foreground="#FFFFFF")
wind.place(x=470,y=420)

rain = Label(text="Rain",font=("arial",14,"bold"),background="#00A1C9",foreground="#FFFFFF")
rain.place(x=650,y=420)



# ----------------------------Labels with values-------------------------------------#


local_time = datetime.now().now()
current_time = local_time.strftime("%I:%M %p")
time_lbl = Label(text=current_time,font=("arial",18),bg="#FFFFFF")
time_lbl.place(x=120,y=150)

temp = Label(text="C°",font=("arial",80,"bold"),bg="#FFFFFF",fg="#ff5050")
temp.place(x=550,y=150)

temp_desc = Label(font=("arial",14,"bold"),bg="#FFFFFF")
temp_desc.place(x=580,y=300)

#---------------------------------------------------------------------------#


humidity_val = Label(font=("arial",12,"bold"),background="#00A1C9")
humidity_val.place(x=230,y=450)

cloud_cover_val = Label( font=("arial",12,"bold"),background="#00A1C9")
cloud_cover_val.place(x=370,y=450)

wind_val = Label( font=("arial",12,"bold"),background="#00A1C9")
wind_val.place(x=500,y=450)

rain_val = Label( font=("arial",12,"bold"),background="#00A1C9")
rain_val.place(x=650,y=450)



#text Field
city = Entry(justify="center",width=17,font=("poppins",25,"bold"),bg="#333333",borderwidth=0,fg="#FFFFFF")
city.place(x=60,y=30)
city.focus()


#-------------------------------- Functions -------------------------------------------#

# convert city into lat long
def city_to_latlon():

        api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.get()}&count=1&language=en&format=json"
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            lat_lng_data = response.json()
            lat = lat_lng_data['results'][0]['latitude']
            lon = lat_lng_data['results'][0]['longitude']
            timezone = lat_lng_data['results'][0]['timezone']

            home = pytz.timezone(timezone)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")

            return lat, lon,current_time
        else:
            return print("Error")

def getWeather():
    lat,lon,current_time = city_to_latlon()
    # Query parameters
    params = {
        "latitude":lat,
        "longitude":lon
    }

    url = "https://api.open-meteo.com/v1/forecast?current=temperature_2m,relative_humidity_2m,wind_speed_10m,is_day,cloud_cover&timezone=auto&daily=rain_sum"

    # Make request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        time_lbl.config(text=f"{current_time}")
        temp.config(text=f"{str(int(data['current']['temperature_2m']))}°")

        cloud_cover = int(data["current"]["cloud_cover"])
        humidity = int(data["current"]['relative_humidity_2m'])
        wind_speed = int(data["current"]['wind_speed_10m'])
        rain = int(data["daily"]['rain_sum'][0])


        humidity_val.config(text=f'{str(humidity) + data["current_units"]["relative_humidity_2m"]}')
        cloud_cover_val.config(text=f'{str(cloud_cover)+data["current_units"]["cloud_cover"]}')
        wind_val.config(text=f'{str(wind_speed)+data["current_units"]["wind_speed_10m"]}')
        rain_val.config(text=f"{str(rain)} mm")


        if cloud_cover >= 70 and humidity >= 70:
            desc= "Cloudy and Humid"
        elif cloud_cover >= 70 and humidity < 70:
            desc = "Cloudy"
        elif cloud_cover < 70 and humidity >= 70:
            desc= "Humid"
        elif rain > 0:
            desc= "Rainy"
        elif wind_speed > 10:
            desc= "Windy"
        else:
            if data["current"]["is_day"]:
                desc= "Sunny"
            else:
                desc= "Clear"

        temp_desc.config(text=desc)


    else:
        print("Error:", response.status_code, response.text)


#--------------------------------------------------------------------------------#

search_icon = Image.open("images/search_icon_white.png")
resized_image = search_icon.resize((45,45))
search_icon = ImageTk.PhotoImage(resized_image)
search_btn = Button(image=search_icon,borderwidth=0,highlightthickness=0,command=getWeather)
search_btn.place(x=390,y=28)

#--------------------------------------------------------------------------------#

window.mainloop()




#--------------------------------------------------------------------------------#
