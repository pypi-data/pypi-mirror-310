import requests
import time

def headIndexEquation(temperature, humidity):
    T = temperature * 9/5 + 32  # Convert Celsius to Fahrenheit
    H = humidity

    # Heat Index equation
    HI = (-42.379 + (2.04901523 * T) + (10.14333127 * H) + (-0.22475541 * T * H) +
                   (-0.00683783 * T * T) + (-0.05481717 * H * H) + (0.00122874 * T * T * H) +
                   (0.00085282 * T * H * H) + (-0.00000199 * T * T * H * H))
    
    return (HI - 32) * 5/9  # Convert back to Celsius


def getPublicAPIDATA(latitude, longitude):
    # URL for Public API Open Meteo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    
    #use the try except to handle the request
    try:
        # send GET request to public API
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # status code check for json response
        if response.status_code == 200:
            data = response.json()  # convert the json response data to dictionary
            
            # get temperature and humidity data
            # handle error for data anomalies
            if 'current_weather' in data and 'temperature' in data['current_weather']:
                current_temperature = data['current_weather']['temperature'] # get temperature data from the list
            else:
                print("ERROR: Temperature data not found")
                return None, None
            
            if 'hourly' in data and 'relativehumidity_2m' in data['hourly']:
                current_humidity = data['hourly']['relativehumidity_2m'][0]  # get humidity data from the list
            else:
                print("ERROR: Humidity data not found") # print the error and return None data to temperature and humidity variable
                return None, None

            return current_temperature, current_humidity # return the data
        else:
            # print this when status code not 200
            # and return None data
            print(f"Error fetching data: {response.status_code}")
            return None, None
    
    # handle for network issues and error
    except requests.ConnectionError:
        print("Error: Unable to connect to the API.")
    except requests.Timeout:
        print("Error: The request timed out.")
    except requests.RequestException as e:
        print(f"Error: An unexpected error occurred: {e}")
    except ValueError:
        print("Error: Unable to parse the response as JSON.")
    
    return None, None  # Return None if any error occurred

    

def main(latitude, longitude):
    while True: # infinite loop 

        # create variable and call the function to get data from public API
        # pass the parameter passed from the main function to the getPublicAPIDATA function
        temperature, humidity = getPublicAPIDATA(latitude, longitude)
        
        # statement for check temperature and humidity
        if temperature is not None and humidity is not None:
            heat_index = headIndexEquation(temperature, humidity)
            # print the the result for the temperature, humidity and Heat Index data
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Heat Index: {heat_index:.2f}°C")
            print("--------------------------------")
        time.sleep(10)  # wait for 10 minutes to make request again


if __name__ == "__main__":
    # coordinates from my actual location
    latitude = -8.55309646857836 # latitude
    longitude = 125.5523432617644 # longitude
    main(latitude, longitude) # run the main function and pass data to main function from the given parameter
