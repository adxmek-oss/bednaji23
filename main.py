import json
import network
import urequests
import utime

# WiFi credentials
WIFI_SSID = "MQTT3IT"
WIFI_PASSWORD = "vyuka3ITmqtt"
OPENWEATHER_API_KEY = "28df0c7072d5262a17a2c651ed2e4cb6"

def connect_to_wifi():
    print("Connecting to WiFi...")
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    utime.sleep(1)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    timeout = 20
    start = utime.time()
    
    while not wlan.isconnected() and (utime.time() - start) < timeout:
        print(".", end="")
        utime.sleep(0.5)
    
    print()
    
    if wlan.isconnected():
        print("Connected to " + WIFI_SSID)
        ip_info = wlan.ifconfig()
        print("IP: " + ip_info[0])
        return True
    else:
        print("Failed to connect to WiFi")
        return False

def get_location_from_ip():
    try:
        print("Getting location...")
        response = urequests.get('https://ip-api.com/json/')
        data = response.json()
        response.close()
        
        print("Raw response: " + str(data))
        
        location = {
            'city': data.get('city'),
            'regionName': data.get('regionName'),
            'country': data.get('country'),
            'latitude': data.get('lat'),
            'longitude': data.get('lon'),
            'ip': data.get('query')
        }
        
        print("City: " + str(location['city']))
        print("Region: " + str(location['regionName']))
        print("Country: " + str(location['country']))
        print("Latitude: " + str(location['latitude']))
        print("Longitude: " + str(location['longitude']))
        
        return location
    
    except Exception as e:
        print("Error getting location: " + str(e))
        return None

def get_weather(latitude, longitude):
    try:
        print("Fetching weather...")
        
        url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=" + OPENWEATHER_API_KEY + "&units=metric"
        
        response = urequests.get(url)
        weather_data = response.json()
        response.close()
        
        if 'main' in weather_data:
            return weather_data
        else:
            print("Invalid response from OpenWeatherMap")
            return None
    
    except Exception as e:
        print("Error fetching weather: " + str(e))
        return None

def display_weather(location, weather_data):
    if not weather_data or 'main' not in weather_data:
        print("Could not retrieve weather data")
        return
    
    main = weather_data['main']
    weather = weather_data['weather'][0]
    wind = weather_data['wind']
    
    city_name = location['city']
    if city_name is None:
        city_name = "Unknown"
    
    region_name = location['regionName']
    if region_name is None:
        region_name = "Unknown"
    
    print("==================================================")
    print("CURRENT WEATHER")
    print("==================================================")
    print("Location: " + str(city_name) + ", " + str(region_name))
    print("--------------------------------------------------")
    temp_str = str(main['temp'])
    feels_str = str(main['feels_like'])
    print("Temp: " + temp_str + "C (feels " + feels_str + "C)")
    print("Humidity: " + str(main['humidity']) + "%")
    print("Pressure: " + str(main['pressure']) + " hPa")
    wind_speed = wind.get('speed', 0)
    print("Wind: " + str(wind_speed) + " m/s")
    print("Conditions: " + weather['main'] + " - " + weather['description'])
    print("==================================================")

def main():
    print("Pi Pico Weather Display")
    print("")
    
    if not connect_to_wifi():
        print("Cannot proceed without WiFi connection")
        return
    
    utime.sleep(2)
    
    location = get_location_from_ip()
    if not location:
        print("Failed to get location")
        return
    
    weather_data = get_weather(location['latitude'], location['longitude'])
    display_weather(location, weather_data)
    
    print("Done!")

main()