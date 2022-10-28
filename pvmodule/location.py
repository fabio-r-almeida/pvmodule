class Location():
    def __init__(self):
        self.city = None  # city
        self.latitude = None  # latitude
        self.longitude = None  # longitude
        self.elevation = None  # elevation
        self.timezone = None  # timezone
        self.name = None  # name

    def set_location(
        self,
        city: str,
        latitude: float = None,
        longitude: float = None,
        elevation: float = None,
        timezone: str = None,
        name: str = None,
    ) -> object:
        """
        Using the city name, this method will geolocate its coordinates, elevation, timezone.
        To use costum locations, just input the desired parameters and they will overwrite the geolocation.
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
