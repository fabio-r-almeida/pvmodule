#@title Simulation class { display-mode: "form" }
class Simulation():
  #def __init__(self):


  def simulate(self,module, location,inverter=None, ac_losses:float=0, dc_losses:bool=False, duration:int = 1, startyear:int = 2005, surface_tilt:float=35, surface_azimuth:float=0, wind:bool=True, download:bool=False, temp:bool=False, isolated_module:bool=False ):
      """
      This method simulates the AC Power and DC Power a system would provide to the grid, using a provided module and a provided inverter (for AC Power). The efficiency for the inverter is calculated using the methos described here: https://www.nrel.gov/docs/fy15osti/64102.pdf
      
      Parameters
      ----------
      location: Location.location
        The location of the desired simulation
      startyear:int , default= 2005
        The startyear of the simulation. When using PVGIS API V5_2, it can go from 2005 to 2020. If wind information if missing, it will use API v5_1 and therefore only go from 2005 to 2016. (this might depend on the location and database data available)
      surface_tilt:float , default=35
        The tilt of the module. This data is being used to fetch real-world data from PVGIS API (degrees)
      surface_azimuth:float , default=35
        The azimuth of the module. This data is being used to fetch real-world data from PVGIS API (degrees)
      duration:int, default= 1
        The duration of the simulation. This will can only be as long as there is available data.
      module :  DataFrame.dtype
          Photovoltaic module, can be parameterized using the method:
            module()
      inverter:
          Dataframe with all the inverter characteristics. Can be selected using:
              list_inverters() -> select_inverters()
      dc_losses:bool, default=False
          Setting this to true will include losses on the DC side of the system.
          The default value for the losses are zero, has to be changed in the module parameters.
          This value if in percentage
      ac_losses: float, default=0
          Setting this to true will include losses on the AD side of the system.
          The default value for the losses are zero. 
          This value if in percentage.
      wind:bool, default=False
          Setting this to True will include wind cooling effects on the module.
          wind_speed has to be provided (dataframe)
      wind_speed :  DataFrame.dtype
          Dataframe that includes the wind speed.
      """
     
      from pvmodule.pvgis import PVGIS
      from pvmodule.system import System
      from pvmodule.inverter import Inverters

      if inverter == None:
        inverter = Inverters().auto_select_inverter(module)
        if len(inverter) <= 0:
          return print('No inverter provided.')

      if startyear < 2005 or startyear > 2020:
        return print('Startyear must be between 2005 and 2020')

      input, output, metadata = PVGIS().retrieve_hourly(latitude=location.latitude, longitude=location.longitude, surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, startyear = startyear)
      output = output.drop(['H_sun','Int'], axis = 1)

      import pandas as pd
      degradation = []
      degradation_year = []

      ac_system = pd.DataFrame()
      dc_system = pd.DataFrame()

      for year in range(duration):
        if startyear + year > 2020:
          break
        if year == 0 :
          output_year = output[output.index.year == startyear + year]
          degradation.append(100)
          degradation_value = 100
          degradation_year.append(startyear + year)
        elif year == 1:
          output_year = output[output.index.year == startyear + year]
          degradation.append(((1-module['first_year_degradation']/100))*100)
          degradation_value = ((1-module['first_year_degradation']/100))*100
          degradation_year.append(startyear + year)
        else: 
          output_year = output[output.index.year == startyear + year]
          degradation.append(((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100)
          degradation_value = ((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100
          degradation_year.append(startyear + year)
        for month in range(1,13):
          output_month = output_year[output_year.index.month == month]
          system_ac = System().ac_production(module=module, T_amb=output_month['T2m'], Irradiance=output_month['G(i)'], inverter=inverter, ac_losses=ac_losses, dc_losses=dc_losses, wind=wind, wind_speed=output_month['WS10m'],temp=temp, isolated_module= isolated_module)
          system_ac = system_ac * degradation_value/100        
          ac_system = ac_system.append(system_ac)

        degradation_df = pd.DataFrame(degradation,columns=['Module Degradation'])
        degradation_df['Year'] = degradation_year

        if download == True:
          degradation_df.to_csv(r'degradation.csv')
          ac_system.to_csv(r'ac_system.csv')
          with open("ac_system.csv", "r+") as fp:
            existing=fp.read()
            fp.seek(0) #point to first line
            fp.write(f"Latitude: {location.latitude}\nLongitude: {location.longitude}\nAddress: {location.name.replace(',',' ')}\nTimezone: {location.timezone}\n Elevation: {location.elevation}\n\nAC Power - AC Power generated by the whole system. Limited by the inverters maximum capacity\nDC Power - System's theorical maximum DC Power generated (has no limitations)\n Wind Speed- The wind speed at a height of 2m (m/2)\n Cell Temperature - The cell temperature using the Kurtz formula (in case the wind speed is being considered) \n 1 Module AC / 1 Module DC - The Power as if the system has only 1 module\n\n"+existing) # add a line above the previously exiting first line


      return ac_system , degradation_df

  def simulate_vertical(self,module, location, inverter=None, ac_losses:float=0, dc_losses:bool=False, duration:int = 1, startyear:int = 2005, surface_tilt:float=90, surface_azimuth:float=90, wind:bool=True, download:bool=False, temp:bool=False, isolated_module:bool=False ):
      """
      This method simulates the AC Power and DC Power a system would provide to the grid, using a provided module and a provided inverter (for AC Power). The efficiency for the inverter is calculated using the methos described here: https://www.nrel.gov/docs/fy15osti/64102.pdf
      
      Parameters
      ----------
      location: Location.location
        The location of the desired simulation
      startyear:int , default= 2005
        The startyear of the simulation. When using PVGIS API V5_2, it can go from 2005 to 2020. If wind information if missing, it will use API v5_1 and therefore only go from 2005 to 2016. (this might depend on the location and database data available)
      surface_tilt:float , default=90
        The tilt of the module. This data is being used to fetch real-world data from PVGIS API (degrees)
      surface_azimuth:float , default= 90 and -90
        The azimuth of the module. This data is being used to fetch real-world data from PVGIS API (degrees)
      duration:int, default= 1
        The duration of the simulation. This will can only be as long as there is available data.
      module :  DataFrame.dtype
          Photovoltaic module, can be parameterized using the method:
            module()
      inverter:
          Dataframe with all the inverter characteristics. Can be selected using:
              list_inverters() -> select_inverters()
      dc_losses:bool, default=False
          Setting this to true will include losses on the DC side of the system.
          The default value for the losses are zero, has to be changed in the module parameters.
          This value if in percentage
      ac_losses: float, default=0
          Setting this to true will include losses on the AD side of the system.
          The default value for the losses are zero. 
          This value if in percentage.
      wind:bool, default=False
          Setting this to True will include wind cooling effects on the module.
          wind_speed has to be provided (dataframe)
      wind_speed :  DataFrame.dtype
          Dataframe that includes the wind speed.
      """
     
      from pvmodule.pvgis import PVGIS
      from pvmodule.system import System
      from pvmodule.inverter import Inverters

      if inverter == None:
        inverter = Inverters().auto_select_inverter(module)
        if len(inverter) <= 0:
          return print('No inverter provided.')


      if startyear < 2005 or startyear > 2020:
        return print('Startyear must be between 2005 and 2020')

      input1, output1, metadata1 = PVGIS().retrieve_hourly(latitude=location.latitude, longitude=location.longitude, surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, startyear = startyear)
      output1 = output1.drop(['H_sun','Int'], axis = 1)
      
      input2, output2, metadata2 = PVGIS().retrieve_hourly(latitude=location.latitude, longitude=location.longitude, surface_tilt=surface_tilt, surface_azimuth=(surface_azimuth*-1), startyear = startyear)
      output2 = output2.drop(['H_sun','Int'], axis = 1)

      output = output1.add(output2, fill_value=0)
      output = output.mul({'G(i)': 1, 'T2m': 0.5, 'WS10m':0.5})

      import pandas as pd
      degradation = []
      degradation_year = []

      ac_system = pd.DataFrame()
      dc_system = pd.DataFrame()

      for year in range(duration):
        if startyear + year > 2020:
          break
        if year == 0 :
          output_year = output[output.index.year == startyear + year]
          degradation.append(100)
          degradation_value = 100
          degradation_year.append(startyear + year)
        elif year == 1:
          output_year = output[output.index.year == startyear + year]
          degradation.append(((1-module['first_year_degradation']/100))*100)
          degradation_value = ((1-module['first_year_degradation']/100))*100
          degradation_year.append(startyear + year)
        else: 
          output_year = output[output.index.year == startyear + year]
          degradation.append(((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100)
          degradation_value = ((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100
          degradation_year.append(startyear + year)
        for month in range(1,13):
          output_month = output_year[output_year.index.month == month]
          system_ac = System().ac_production(module=module, T_amb=output_month['T2m'], Irradiance=output_month['G(i)'], inverter=inverter, ac_losses=ac_losses, dc_losses=dc_losses, wind=wind, wind_speed=output_month['WS10m'],temp=temp, isolated_module= isolated_module)
          system_ac = system_ac * degradation_value/100        
          ac_system = ac_system.append(system_ac)

        degradation_df = pd.DataFrame(degradation,columns=['Module Degradation'])
        degradation_df['Year'] = degradation_year

        if download == True:
          degradation_df.to_csv(r'degradation.csv')
          ac_system.to_csv(r'ac_system.csv')
          with open("ac_system.csv", "r+") as fp:
            existing=fp.read()
            fp.seek(0) #point to first line
            fp.write(f"Latitude: {location.latitude}\nLongitude: {location.longitude}\nAddress: {location.name.replace(',',' ')}\nTimezone: {location.timezone}\n Elevation: {location.elevation}\n\nAC Power - AC Power generated by the whole system. Limited by the inverters maximum capacity\nDC Power - System's theorical maximum DC Power generated (has no limitations)\n Wind Speed- The wind speed at a height of 2m (m/2)\n Cell Temperature - The cell temperature using the Kurtz formula (in case the wind speed is being considered) \n 1 Module AC / 1 Module DC - The Power as if the system has only 1 module\n\n"+existing) # add a line above the previously exiting first line


      return ac_system , degradation_df