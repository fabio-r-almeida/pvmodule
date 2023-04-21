#@title FINAL (TESE) Simulation class { display-mode: "form" }
class Simulation():
  #def __init__(self):


  def simulate(self,
               module,
               location,
               irradiance,
               duration:int = 5,
               inverter=None,
               ac_losses:float=0,
               dc_losses:bool=True,
               surface_tilt:float=35,
               surface_azimuth:float=0, 
               wind:bool=True,
               download:bool=False,
               temp:bool=False,
               isolated_module:bool=False 
               ):

      from pvmodule.inverter import Inverters

      if inverter == None:
        inverter = Inverters().auto_select_inverter(module)
        if len(inverter) <= 0:
          return print('No suitable inverter found.')


      import pandas as pd
      degradation = []
      degradation_year = []

      ac_system = pd.DataFrame()
      dc_system = pd.DataFrame()
      startyear = int(irradiance.index[0].year)



      for year in range(duration):
        if year == 0 :
          output_year = irradiance[irradiance.index.year == startyear]
          degradation.append(100)
          degradation_value = 100
          degradation_year.append(startyear + year)
        elif year == 1:
          output_year = irradiance[irradiance.index.year == startyear]
          degradation.append(((1-module['first_year_degradation']/100))*100)
          degradation_value = ((1-module['first_year_degradation']/100))*100
          degradation_year.append(startyear + year)
        else:
          output_year = irradiance[irradiance.index.year == startyear]
          degradation.append(((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100)
          degradation_value = ((1-module['first_year_degradation']/100)*(1-module['annual_degradation']/100)**(year-1))*100
          degradation_year.append(startyear + year)


        for month in range(1,13):
          output_month = output_year[output_year.index.month == month]
          #system_ac = System().ac_production(module=module, T_amb=output_month['T2m'], Irradiance=output_month['G(i)'], inverter=inverter, ac_losses=ac_losses, dc_losses=dc_losses, wind=wind, wind_speed=output_month['WS10m'],temp=temp, isolated_module= isolated_module)
          #system_ac = system_ac * degradation_value/100
          #ac_system = ac_system.append(system_ac)

        degradation_df = pd.DataFrame(degradation,columns=['Module Degradation'])
        degradation_df['Year'] = degradation_year

        if download == True:
          degradation_df.to_csv(r'degradation.csv')
          ac_system.to_csv(r'ac_system.csv')
          with open("ac_system.csv", "r+") as fp:
            existing=fp.read()
            fp.seek(0) #point to first line
            fp.write(f"Latitude: {location.latitude}\nLongitude: {location.longitude}\nAddress: {location.name.replace(',',' ')}\nTimezone: {location.timezone}\n Elevation: {location.elevation}\n\nAC Power - AC Power generated by the whole system. Limited by the inverters maximum capacity\nDC Power - System's theorical maximum DC Power generated (has no limitations)\n Wind Speed- The wind speed at a height of 2m (m/2)\n Cell Temperature - The cell temperature using the Kurtz formula (in case the wind speed is being considered) \n 1 Module AC / 1 Module DC - The Power as if the system has only 1 module\n\n"+existing) # add a line above the previously exiting first line


      #return ac_system , degradation_df

  