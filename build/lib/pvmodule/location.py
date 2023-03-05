#@title FINAL (TESE) - Location class { display-mode: "form" }
class Location():
    def __init__(self):
        self.city = None  # city
        self.latitude = None  # latitude
        self.longitude = None  # longitude
        self.elevation = None  # elevation
        self.timezone = None  # timezone
        self.name = None  # name

    def set_location(self, city: str= None, latitude: float = None, longitude: float = None, elevation: float = None, timezone: str = None, name: str = None, ) -> object:
        """
        Using the city name, this method will geolocate its coordinates, elevation, timezone.
        To use costum locations, just input the desired parameters and they will overwrite the geolocation.
        Parameters
        ----------
        city: str
          The name of the city in which the system is going to be built.
        latitude: float, default = None,
          A specific latitude to overwrite the automatic search.
        longitude: float, default = None,
          A specific longitude to overwrite the automatic search.
        elevation: float, default = None,
          A specific elevation to overwrite the automatic search.
          This elevation corresponds to how many meters the city is above the sea-level.
        timezone: str, default = None,
          The timezone in which the city is located.
          A specific timezone to overwrite the automatic search.
        name: str, default = None,
          The name of the system. This does not affect anything.
        """

        #from tzwhere import tzwhere
        #import requests
        #from geopy.geocoders import Nominatim
        #import numpy as np
        #import warnings

        #warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        #self.timezone = timezone
        self.name = name

        #if city != None:
        #  import random
        #  geolocator = Nominatim(user_agent=f"fabio_{random.randrange(1, 900000)}_almeida_{random.randrange(1, 900000)}_thesis{random.randrange(1, 900000)}")
        #  location = geolocator.geocode(str(city))
        #  if self.latitude == None:
        #      self.latitude = location.latitude
        #  if self.longitude == None:
        #      self.longitude = location.longitude
        #  #if self.timezone == None:
        #  #    self.timezone = tzwhere.tzwhere().tzNameAt(location.latitude, location.longitude)
        #  if self.name == None:
        #      try:
        #        self.name = location.address
        #      except:
        #        pass
        #  if self.elevation == None:
        #      try:
        #        url = "https://api.opentopodata.org/v1/eudem25m?"
        #        params = {"locations": f"{location.latitude},{location.longitude}"}
        #        result = requests.get(url, params)
        #        if result.ok:
        #            self.elevation = result.json()["results"][0]["elevation"]
        #        else:
        #            url = "https://api.open-elevation.com/api/v1/lookup?"
        #            params = {"locations": f"{location.latitude},{location.longitude}"}
        #            result = requests.get(url, params)
        #            self.elevation = result.json()["results"][0]["elevation"]
        #      except:
        #        pass
        #else:
        #  import random
        #  geolocator = Nominatim(user_agent=f"fabio_{random.randrange(1, 900000)}_almeida_{random.randrange(1, 900000)}_thesis{random.randrange(1, 900000)}")
        #  latitude_longitude =  str(latitude)+","+  str(longitude)
        #  location = geolocator.reverse(str(latitude_longitude))
        #  self.city = str(location.address)
        #  location = geolocator.geocode(str(location.address))
        #  if self.latitude == None:
        #      self.latitude = location.latitude
        #  if self.longitude == None:
        #      self.longitude = location.longitude
        #  #if self.timezone == None:
        #  #    self.timezone = tzwhere.tzwhere().tzNameAt(location.latitude, location.longitude)
        #  if self.name == None:
        #      try:
        #        self.name = location.address
        #      except:
        #        pass
        #  if self.elevation == None:
        #      try:
        #        url = "https://api.opentopodata.org/v1/eudem25m?"
        #        params = {"locations": f"{location.latitude},{location.longitude}"}
        #        result = requests.get(url, params)
        #        if result.ok:
        #            self.elevation = result.json()["results"][0]["elevation"]
        #        else:
        #            url = "https://api.open-elevation.com/api/v1/lookup?"
        #            params = {"locations": f"{location.latitude},{location.longitude}"}
        #            result = requests.get(url, params)
        #            self.elevation = result.json()["results"][0]["elevation"]
        #      except:
        #        pass
        return self

    def get_info(self, location):

      return {
          'Address':location.name,
          'Latitude':location.latitude,
          'Longitude':location.longitude,
          'Elevation':location.elevation
          #'Timezone':location.timezone
          }