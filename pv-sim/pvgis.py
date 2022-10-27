class PVGIS():
  def __init__(self):
    #hourly
    self.latitude=None,#latitude
    self.longitude=None,#longitude
    self.usehorizon=None,#usehorizon
    self.userhorizon=None,#userhorizon
    self.raddatabase=None,#raddatabase
    self.startyear=None,#startyear
    self.endyear =None,#endyear
    self.pvcalculation=None,#pvcalculation
    self.peakpower= None,#peakpower
    self.pvtechchoice=None,#pvtechchoice
    self.mountingplace=None,#mountingplace
    self.loss=None,#loss
    self.trackingtype=None,#trackingtype
    self.surface_tilt=None,#surface_tilt
    self.surface_azimuth=None,#surface_azimuth
    self.optimalinclination=None,#optimalinclination
    self.optimalangles=None,#optimalangles
    self.components=None,#components
    self.outputformat=None,#outputformat
    self.url=None,#url
    self.data = None
    #monthly
    self.horirrad = None,#horirrad
    self.optrad = None,#optrad
    self.selectrad = None,#selectrad
    self.angle = None,#angle
    self.mr_dni = None,#mr_dni
    self.d2g = None,#d2g
    self.avtemp = None,#avtemp
    #daily
    self.month = None,#month
    self.angle= None,#angle
    self.aspect =None,#aspect
    self.global_irr =None,# global_irr
    self.glob_2axis = None,#glob_2axis
    self.clearsky = None,#clearsky
    self.clearsky_2axis =None, #clearsky_2axis
    self.showtemperatures=None#,showtemperatures
    self.localtime=None,#localtime



  def retrieve_hourly(self, latitude,longitude,usehorizon=1,userhorizon=None,raddatabase=None, startyear=None, endyear = None, pvcalculation=0, peakpower=None, pvtechchoice="crystSi", mountingplace="free", loss=None, trackingtype=0, surface_tilt=0, surface_azimuth=0, optimalinclination=0, optimalangles=0, components=0, outputformat='json', url='http://re.jrc.ec.europa.eu/api/v5_2/' ):
    
    import requests
    import pandas as pd
    import json

    self.latitude=latitude
    self.longitude=longitude
    self.usehorizon=usehorizon
    self.userhorizon=userhorizon
    self.raddatabase= raddatabase
    self.startyear=startyear
    self.endyear =endyear
    self.pvcalculation=pvcalculation
    self.peakpower= peakpower
    self.pvtechchoice=pvtechchoice
    self.mountingplace=mountingplace
    self.loss=loss
    self.trackingtype=trackingtype
    self.surface_tilt=surface_tilt
    self.surface_azimuth=surface_azimuth
    self.optimalinclination=optimalinclination
    self.optimalangles=optimalangles
    self.components=components
    self.outputformat=outputformat
    self.url=url
    self.data = None

    url = self.url + f'seriescalc?lat={self.latitude}&lon={self.longitude}'

    if(self.usehorizon != None):
      url = url + f'&usehorizon={self.usehorizon}'
    if(self.userhorizon != None):
      url = url + f'&userhorizon={self.userhorizon}'
    if(self.raddatabase != None):
      url = url + f'&raddatabase={self.raddatabase}'
    if(self.startyear != None):
      url = url + f'&startyear={self.startyear}'
    if(self.endyear != None):
      url = url + f'&endyear={self.endyear}'
    if(self.pvcalculation != None):
      url = url + f'&pvcalculation={self.pvcalculation}'
    if(self.peakpower != None):
      url = url + f'&peakpower={self.peakpower}'
    if(self.pvtechchoice != None):
      url = url + f'&pvtechchoice={self.pvtechchoice}'
    if(self.mountingplace != None):
      url = url + f'&mountingplace={self.mountingplace}'
    if(self.loss != None):
      url = url + f'&loss={self.loss}'
    if(self.trackingtype != None):
      url = url + f'&trackingtype={self.trackingtype}'
    if(self.surface_tilt != None):
      url = url + f'&surface_tilt={self.surface_tilt}'
    if(self.surface_azimuth != None):
      url = url + f'&surface_azimuth={self.surface_azimuth}'
    if(self.optimalinclination != None):
      url = url + f'&optimalinclination={self.optimalinclination}'
    if(self.optimalangles != None):
      url = url + f'&optimalangles={self.optimalangles}'
    if(self.components != None):
      url = url + f'&components={self.components}'
    if(self.outputformat != None):
      url = url + f'&outputformat={self.outputformat}'

    self.url = url
    data = requests.get(url).json()
    try:
      outputs = data['outputs']['hourly']
      outputs = pd.json_normalize(outputs)
      outputs['time'] = pd.to_datetime(outputs.time, format='%Y%m%d:%H%M')
      outputs = outputs.set_index('time')

      inputs = data['inputs']

      meta = data['meta']
    except:
      return print(f'Error: {data}')


    self.data = outputs, inputs, meta
    return self.data

  def retrieve_monthly(self, latitude, longitude, usehorizon=1,userhorizon=None, raddatabase=None, startyear=None, endyear = None, horirrad=1, optrad=0, selectrad=0, angle=0, mr_dni=1, d2g=1, avtemp=1, outputformat='json', url='http://re.jrc.ec.europa.eu/api/v5_2/'):
    
    import requests
    import pandas as pd
    import json

    self.latitude=latitude
    self.longitude=longitude
    self.usehorizon=usehorizon
    self.userhorizon=userhorizon
    self.raddatabase= raddatabase
    self.startyear=startyear
    self.endyear =endyear
    self.horirrad = horirrad
    self.selectrad = selectrad
    self.angle = angle
    self.mr_dni = mr_dni
    self.d2g=d2g
    self.avtemp=avtemp
    self.outputformat=outputformat
    self.url=url
    self.data = None

    url = self.url + f'MRcalc?lat={self.latitude}&lon={self.longitude}'

    if(self.usehorizon != None):
      url = url + f'&usehorizon={self.usehorizon}'
    if(self.userhorizon != None):
      url = url + f'&userhorizon={self.userhorizon}'
    if(self.raddatabase != None):
      url = url + f'&raddatabase={self.raddatabase}'
    if(self.startyear != None):
      url = url + f'&startyear={self.startyear}'
    if(self.endyear != None):
      url = url + f'&endyear={self.endyear}'
    if(self.horirrad != None):
      url = url + f'&horirrad={self.horirrad}'
    if(self.selectrad != None):
      url = url + f'&selectrad={self.selectrad}'
    if(self.angle != None):
      url = url + f'&angle={self.angle}'
    if(self.mr_dni != None):
      url = url + f'&mr_dni={self.mr_dni}'
    if(self.avtemp != None):
      url = url + f'&avtemp={self.avtemp}'
    if(self.d2g != None):
      url = url + f'&d2g={self.d2g}'
    if(self.outputformat != None):
      url = url + f'&outputformat={self.outputformat}'

    self.url = url
    data = requests.get(url).json()
    try:
      outputs = data['outputs']['monthly']
      outputs = pd.json_normalize(outputs)

      inputs = data['inputs']

      meta = data['meta']
    except:
      return print(f'Error: {data}')


    self.data = outputs, inputs, meta
    return self.data

  def retrieve_daily(self, latitude, longitude, month, usehorizon=1, userhorizon = None, raddatabase=None, angle=0, aspect = 0, global_irr = 1, glob_2axis = 0, clearsky = 0, clearsky_2axis = 0, showtemperatures = 1, localtime = 1, outputformat='json', url='http://re.jrc.ec.europa.eu/api/v5_2/'):
    
    import requests
    import pandas as pd
    import json

    self.month = month
    self.latitude=latitude
    self.longitude=longitude
    self.usehorizon=usehorizon
    self.userhorizon=userhorizon
    self.raddatabase= raddatabase
    self.angle=angle
    self.aspect =aspect
    self.global_irr = global_irr
    self.glob_2axis = glob_2axis
    self.clearsky = clearsky
    self.clearsky_2axis = clearsky_2axis
    self.showtemperatures=showtemperatures
    self.localtime=localtime
    self.outputformat=outputformat
    self.url=url
    self.data = None

    url = self.url + f'DRcalc?lat={self.latitude}&lon={self.longitude}&month={self.month}'

    if(self.usehorizon != None):
      url = url + f'&usehorizon={self.usehorizon}'
    if(self.userhorizon != None):
      url = url + f'&userhorizon={self.userhorizon}'
    if(self.raddatabase != None):
      url = url + f'&raddatabase={self.raddatabase}'
    if(self.angle != None):
      url = url + f'&angle={self.angle}'
    if(self.aspect != None):
      url = url + f'&aspect={self.aspect}'
    if(self.global_irr != None):
      url = url + f'&global={self.global_irr}'
    if(self.glob_2axis != None):
      url = url + f'&glob_2axis={self.glob_2axis}'
    if(self.clearsky != None):
      url = url + f'&clearsky={self.clearsky}'
    if(self.clearsky_2axis != None):
      url = url + f'&clearsky_2axis={self.clearsky_2axis}'
    if(self.showtemperatures != None):
      url = url + f'&showtemperatures={self.showtemperatures}'
    if(self.localtime != None):
      url = url + f'&localtime={self.localtime}'
    if(self.outputformat != None):
      url = url + f'&outputformat={self.outputformat}'

    self.url = url
    data = requests.get(url).json()
    try:
      outputs = data['outputs']['daily_profile']
      outputs = pd.json_normalize(outputs)
      outputs = outputs.set_index('time')

      inputs = data['inputs']

      meta = data['meta']

    except:
      return print(f'Error: {data}')


    self.data = outputs, inputs, meta
    return self.data