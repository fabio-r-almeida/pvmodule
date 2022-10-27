class Location():
  def __init__(self):
    '''
    city: Name of the city
    latitude: latitude of the location, if not known, it should be let empty or None
    longitude: longitude of the location, if not known, it should be let empty or None
    elevation: elevation of the location, if not known, it should be let empty or None
    timezone: timezone of the location, if not known, it should be let empty or None
    name: Name of the location, if this value is nome, it will be renamed the address 
    '''
    self.city = None,#city
    self.latitude = None,#latitude
    self.longitude = None,#longitude
    self.elevation = None,#elevation
    self.timezone = None,#timezone
    self.name = None,#name

  def set_location(self, city, latitude=None, longitude=None, elevation=None, timezone=None, name=None):
   
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

    geolocator =  Nominatim(user_agent="fabio_almeida_thesis")
    location = geolocator.geocode(str(self.city))
    if(self.latitude == None):
      self.latitude = location.latitude
    if(self.longitude == None):
      self.longitude = location.longitude
    if(self.timezone == None):
      self.timezone = tzwhere.tzwhere().tzNameAt(self.latitude, self.longitude)
    if(self.name == None):
      self.name = location.address
    if(self.elevation == None):
      url = 'https://api.opentopodata.org/v1/eudem25m?'
      params = {'locations': f"{self.latitude},{self.longitude}"}
      result = requests.get(url, params)
      if result.ok:
        self.elevation = result.json()['results'][0]['elevation']
      else:
        url = 'https://api.open-elevation.com/api/v1/lookup?'
        params = {'locations': f"{self.latitude},{self.longitude}"}
        result = requests.get(url, params)
        self.elevation = result.json()['results'][0]['elevation']

    return self