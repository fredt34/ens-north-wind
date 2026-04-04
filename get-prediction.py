import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Fake edit 1,2

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 48.8627,
	"longitude": 2.2875,
	"hourly": ["wind_speed_80m", "wind_direction_80m", "temperature_80m"],
	"utm_source": "chatgpt.com",
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_wind_speed_80m = hourly.Variables(0).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(1).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["temperature_80m"] = hourly_temperature_80m

hourly_dataframe = pd.DataFrame(data = hourly_data)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_cols", None)
print("\nHourly data\n", hourly_dataframe)
