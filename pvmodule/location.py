#@title FINAL (TESE) - Location class { display-mode: "form" }
class Location():
    def __init__(self):
        self.city = None  # city
        self.latitude = None  # latitude
        self.longitude = None  # longitude
        self.elevation = None  # elevation
        self.timezone = None  # timezone
        self.name = None  # name

    def set_location(self, city: str, latitude: float = None, longitude: float = None, elevation: float = None, timezone: str = None, name: str = None, ) -> object:
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

        from tzwhere import tzwhere
        import requests
        from geopy.geocoders import Nominatim
        import numpy as np
        import warnings

        warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.timezone = timezone
        self.name = name

        geolocator = Nominatim(user_agent="fabio_almeida_thesis")
        location = geolocator.geocode(str(self.city))
        if self.latitude == None:
            self.latitude = location.latitude
        if self.longitude == None:
            self.longitude = location.longitude
        if self.timezone == None:
            self.timezone = tzwhere.tzwhere().tzNameAt(self.latitude, self.longitude)
        if self.name == None:
            self.name = location.address
        if self.elevation == None:
            url = "https://api.opentopodata.org/v1/eudem25m?"
            params = {"locations": f"{self.latitude},{self.longitude}"}
            result = requests.get(url, params)
            if result.ok:
                self.elevation = result.json()["results"][0]["elevation"]
            else:
                url = "https://api.open-elevation.com/api/v1/lookup?"
                params = {"locations": f"{self.latitude},{self.longitude}"}
                result = requests.get(url, params)
                self.elevation = result.json()["results"][0]["elevation"]

        return self

    def get_info(location):

      return {
          'Address':location.name,
          'Latitude':location.latitude,
          'Longitude':location.longitude,
          'Elevation':location.elevation,
          'Timezone':location.timezone,
          }
