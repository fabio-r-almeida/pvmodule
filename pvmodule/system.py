#@title System function
class System():
    def __init__(self):
        self.spacing = None
        self.plot_height = None
        self.plot_length = None
        self.total_modules = None
        self.modules_per_string = 1
        self.number_of_strings = 1
        self.name = None
        self.height = None
        self.length = None
        self.width = None
        self.pdc = None
        self.umpp = None
        self.impp = None
        self.uoc = None
        self.isc = None
        self.NOCT = None
        self.tc_pmax = None
        self.tc_voc = None
        self.tc_isc = None
        self.losses = None

    def __modules_spacing(self, MHeight: float, tilt: float, n_year: int = None, latitude: float = None) -> float:
        """
        This method calculates the necessary spacing between modules to eliminate shading/parcial shading.
        To calculate the worst-case scenario, use only:
          MHeight - height of the module (meters)
          tilt - surface tilt of the module (degree)

        To calculate for a specific time of the year, use in addition
          n_year - the day in the year
          latitude - latitude of the system
        """
        import math

        if n_year == None or latitude == None:
            self.spacing = round(MHeight * ( math.cos(tilt * math.pi / 180) + (math.sin(tilt * math.pi / 180)) / (math.tan(23.45 * math.pi / 180)) ), 3, )

        else:
            beta = 23.45 * math.sin((360 / 365) * math.pi / 180) * (n_year - 81)
            beta_n = 90 - latitude + beta
            self.spacing = round( MHeight * ( math.cos(tilt * math.pi / 180) + (math.sin(tilt * math.pi / 180)) / (math.tan(beta_n)) ), 3, )
        return self.spacing

    #def __module_quantity(self, MLength, MHeight, PLength, PHeight, tilt):
    #    """
    #    :MLength : Module config Length
    #    :MHeight : Module config Height
    #    :PLength : Plot config Length
    #    :PHeight : Plot config Height
    #    :Inclination: Module Inclination
    #    """
    #    import math
#
    #    modules_in_string = math.floor(PLength / MLength)
    #    modules_spacing = __modules_spacing(MHeight, tilt)
    #    number_of_strings = math.floor(PHeight / modules_spacing)
#
    #    self.total_modules = modules_in_string * number_of_strings
    #    self.modules_per_string = modules_in_string
    #    self.number_of_strings = number_of_strings
#
    #    return self.total_modules, self.modules_per_string, self.number_of_strings

    def module(self, name: str = "LG_Neon_2_ LG350N1C-V5", height: float = 1.686, length: float = 1.016, width: float = 40, pdc: float = 350, umpp: float = 35.3, impp: float = 9.92, uoc: float = 41.3, isc: float = 10.61, NOCT: float = 42, efficiency:float = 20.4, tc_pmax: float = -0.36, tc_voc: float = -0.27, tc_isc: float = 0.03, modules_per_string:int=1, number_of_strings:int=1, losses:float=0,first_year_degradation:float=2, annual_degradation:float=0.33 ) -> dict:
      """
      This method defines the module used for the calculations.
      The standarts module is the LG_Neon_2_ LG350N1C-V5 with the following specsheet:
      Datasheet
      ---------
        Name ='LG_Neon_2_ LG350N1C-V5',
        Height (meters) : 1.686,
        Length (meters) : 1.016,
        Width (meters) : 0.040,
        Pdc (Watt) : 350,
        Umpp (Volt) : 35.3,
        Impp (A) : 9.92,
        Uoc (V) : 41.3,
        Isc (A): 10.61,
        NOCT (ºC) : 42,
        Efficiency (%) : 20.4
        Tc_pmax (%/ºC) : -0.36,
        Tc_voc (%/ºC) : -0.27,
        Tc_isc (%/ºC) : 0.03,
        losses (%) : 0
        first_year_degradation (%) : 2%
        annual_degradation (%) : 0.33%
      """

      self.name = name
      self.height = height
      self.length = length
      self.width = width
      self.pdc = pdc
      self.umpp = umpp
      self.impp = impp
      self.uoc = uoc
      self.isc = isc
      self.NOCT = NOCT
      self.efficiency = efficiency
      self.tc_pmax = tc_pmax
      self.tc_voc = tc_voc
      self.tc_isc = tc_isc
      self.modules_per_string = modules_per_string
      self.number_of_strings = number_of_strings
      self.losses = losses
      self.first_year_degradation =first_year_degradation
      self.annual_degradation = annual_degradation

      return {
          'name':self.name,
          'height':self.height,
          'length':self.length,
          'width':self.width,
          'pdc':self.pdc,
          'umpp':self.umpp,
          'impp':self.impp,
          'uoc':self.uoc,
          'isc':self.isc,
          'NOCT':self.NOCT,
          'efficiency':self.efficiency,
          'tc_pmax':self.tc_pmax,
          'tc_voc':self.tc_voc,
          'tc_isc':self.tc_isc,
          'modules_per_string':self.modules_per_string,
          'number_of_strings':self.number_of_strings,
          'losses':self.losses,
          'first_year_degradation':self.first_year_degradation,
          'annual_degradation':self.annual_degradation
          
          }
        
############################################
# DC Power calculation.

    def _Tcell(self, module, T_amb, Irradiance, wind_speed):
        #Kurtz - https://pdf.sciencedirectassets.com/277910/1-s2.0-S1876610213X00104/1-s2.0-S1876610213016044/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQC8KgfYrZdUnt7dMO4KJXbgrhHk5QU4ZYGTevVJaz26vQIhAJWcPNCzwINErnCW8XmhYmmi6h87fdKdQ4c6YCxi4ccRKswECEIQBRoMMDU5MDAzNTQ2ODY1IgwnJmllX8y0kAHLrrAqqQQsVDEGiXuqmbwz1YbBbNgCJwQlcRTRJh13IYb8f4k%2BWOAxjyASlwZ0w1kJX4suaWtUHOfXlskEosm09dh2NX1xNysJ3NwlYMPTHQafDK2%2Fg3g7Zc8DIDw9H2TwqI3kN4rx4YkKb72Rqb9GSIbsfDYtubI%2BACL1ajeIr1idCQ%2F2OefyA%2B%2Fw3siLEthT%2BBnJpYDwc4QqhKG8eewdkJwjvJJyQxnPsFfJf72j0wQcUQ0E6xKju1hFZVgQFXFUDP0onXZJr1w6nYmSJp3phHAuseqKoLWHhCuKy0oVUAxZqT9lkEt6wVWrqPQHJQTUfGU8PlBYKAoMZX457IfHgJU1htpOiEmVBQcnP9uQ%2BKO2sMfEE9JmBZwmMD2XnolOJ2p26%2FgUCwXqbN9EwYBQAYo4SYDLn9n24sVavaMrIf9ZqS5HC34LHNe7tvPcEC0J0mHfhzvzUguT93L0mcBq3nHiEgiTVr5JAgYNIPs0Usuj6ObzpIPzK2dWpOnNcAIfns0PayNSpRcNFGiLvW4tCj0Lfq9fxj21aygbHxeOWIXcu32UvghcQMpOAryMJKDcTaWdBlJNJthX2L5n9epY%2BvuioLVtnYjEyIulokBUWUApz8GJaIX6MFv8kh7iGHiDELEpCLghXBU%2Fo%2F7Kqq3dFiXakWrIFHLFiR%2BPbj3iR%2FikYtt1d1NBXpS4Eb2UWCs0oSPigRzmZooPxSQRVYZzqIEdFfFjKkt%2FmjgjXvzfMJ3X85oGOqgBxHDP1OZMxNmHh8neGyQSrtRnFgRB3I0MArd%2BFFPGdNCy76zqcpGb0FSDGNecPpAdFU8V0x%2FrxWrfuYi3RFi0wEplxj11GkRDnrZhmyTzIXA%2BHDAYhorAVUFLWDMRJ4N0Dune077ee5Abs6qxLp%2FjfG61lEslhUvH4tW3GQTI6VgSqbZXjpvzoRcHnDSmVbZV7vKPpqkT3HbPlrGdGf%2FTtoT6M5WOC%2BKk&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221029T092527Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYW7235T6G%2F20221029%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=9c4646596a060c4f3be2149c2fa429c590dcebc5240246f15d308cdb3384a9cc&hash=802d1c967efca932ba4387d0f917156d45726685192d8dfbc0dcc9187c0ab7aa&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1876610213016044&tid=spdf-cb1126c0-67cf-43ee-97cb-272f614a6620&sid=8be7f42727776347ad1a55b471ecb6d1ac82gxrqb&type=client&ua=4d545307060057000602&rr=761add2fcb2169b9
        
        #converts the 10m to 2m wind (meter for the height of the panels).
        from math import log, e
        wind_speed_2m = wind_speed * 4.87 /  log(67.8*10 - 5.42)

        Tc_kurtz_2m =  T_amb + Irradiance*e**(-3.473-0.0594*wind_speed_2m)

        return Tc_kurtz_2m, wind_speed_2m




    def _dc_production(self,module, T_amb, Irradiance,Temp,Isolated_module, wind, wind_speed):
      import pandas as pd
      import math

      if wind == False:
        T_cell = T_amb + (module['NOCT'] - 20) / 800 * Irradiance
      else:
        T_cell, wind_speed = System()._Tcell(module, T_amb, Irradiance, wind_speed)
      
      Pdc_max = module['pdc'] * Irradiance / 1000
      delta_T = T_cell - 25
      PV = Pdc_max * (1 + module['tc_pmax'] / 100 * delta_T)
        

      estimated_current = module['isc']*Irradiance/1000

      dc_prod = PV * (module['modules_per_string']*module['number_of_strings'])
      dc_prod = pd.DataFrame(dc_prod)
      dc_prod.columns = ['DC Power']
      dc_prod['G(i)'] = Irradiance
      dc_prod['U (V)'] = PV/estimated_current
      dc_prod['I (A)'] = estimated_current
      dc_prod = dc_prod.fillna(0)
      if Temp == True:
        dc_prod['Cell Temperature'] = T_cell
      if Isolated_module == True:
        dc_prod['1 DC Module'] = PV 
      if wind == True:
        dc_prod['Wind Speed'] = wind_speed 


      return dc_prod

    def _dc_production_losses(self,dc_prod, losses):
      if losses != type(float) or losses != type(int):
        return dc_prod
      else:
        return dc_prod * (1 - losses)


    def dc_production(self, module, T_amb, Irradiance, temp:bool=False, isolated_module:bool=False, dc_losses:bool=False, wind:bool=False,wind_speed=None):
      """
      This method calculates the DC Power a system would output.
      Parameters
      ----------
      module :  DataFrame.dtype
          Photovoltaic module, can be parameterized using the method:
            module()
      T_amb:  DataFrame.series
          Dataframe with the temperatures. Can be retrieved using PVGIS
      Irradiance:
          Dataframe with the Irradiance on the photovoltaic surface. Can be retrieved using PVGIS.
      dc_losses:bool, default=False
          Setting this to true will include losses on the DC side of the system.
          The default value for the losses are zero, has to be changed in the module parameters.
          This value if in percentage
      temp:bool, default=False
          Setting this to True will add an extra column to the output (the temperature column)
      isolated_module:bool, default=False
          Setting this to True will add an extra column to the output, as if the system were to be run only using one module.
          This is not affected by the inverter efficiency. (AC == DC)
      wind:bool, default=False
          Setting this to True will include wind cooling effects on the module.
          wind_speed has to be provided (dataframe)
      wind_speed :  DataFrame.dtype
          Dataframe that includes the wind speed.
      """

      dc_prod = System()._dc_production(module, T_amb, Irradiance,temp ,isolated_module, wind, wind_speed)
      self.dc_prod = dc_prod
      if dc_losses == True:
        dc_prod_losses = System()._dc_production_losses(dc_prod, module['losses'])
        self.dc_prod = dc_prod_losses

      return self.dc_prod

############################################
# AC Power calculation based on a inverter from the CECInverter list provided by CEC.

    def _ac_production_inverter(self, inverter ,v_dc ,p_dc):
      import pandas as pd

      Paco = float(inverter['Paco'])
      Pnt = float(inverter['Pnt'])
      Pso = float(inverter['Pso'])

      power_ac = System()._efficiency(v_dc, p_dc, inverter)      
      power_ac = System()._limits_power(power_ac, p_dc, Paco, Pnt, Pso)

      if isinstance(p_dc, pd.Series):
          power_ac = pd.Series(power_ac, index=p_dc.index)

      return power_ac

    def _efficiency(self, v_dc, p_dc, inverter):
      '''
      Calculate the inverter AC power
      credits: https://www.nrel.gov/docs/fy15osti/64102.pdf
      '''
      Paco = float(inverter['Paco'])
      Pdco = float(inverter['Pdco'])
      Vdco = float(inverter['Vdco'])
      C0 = float(inverter['C0'])
      C1 = float(inverter['C1'])
      C2 = float(inverter['C2'])
      C3 = float(inverter['C3'])
      Pso = float(inverter['Pso'])

      A = Pdco * (1 + C1 * (v_dc - Vdco))
      B = Pso * (1 + C2 * (v_dc - Vdco))
      C = C0 * (1 + C3 * (v_dc - Vdco))

      return (Paco / (A - B) - C * (A - B)) * (p_dc - B) + C * (p_dc - B)**2

    def _limits_power(self, power_ac, p_dc, Paco, Pnt, Pso):
      '''
      Applies maximum power limits to the ac power depending on the selected inverter.
      '''
      import numpy as np

      power_ac = np.minimum(Paco, power_ac)
      min_ac_power = -1.0 * abs(Pnt)
      below_limit = p_dc < Pso

      try:
          power_ac[below_limit] = min_ac_power
      except TypeError:  
          if below_limit:
              power_ac = min_ac_power

      return power_ac

    def list_inverters(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'):
      """
      List of inverters provided by CEC.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      """
      import pandas as pd
      inverters = pd.read_csv(url).replace(" ", "")

      return inverters

    def select_inverter(self, name:str, list):
      """
      Select the inverter from a provided list.
      To access the list, please use the method:
        list_inverters()

      Parameters
      ----------
      name : str
          The name of the inverter, as listed on the list.

      list : DataFrame.dtype
          A list with the inverter and its specifications.
      """

      return list.loc[list['Name'] == name]



    def ac_production(self, module, T_amb, Irradiance, inverter, ac_losses:float=0, temp:bool=False, isolated_module:bool=False, dc_losses:bool=False, wind:bool=False,wind_speed=None):
      """
      This method calculates the AC Power a system would provide to the grid, using a provided module and a provided inverter. The efficiency for the inverter is calculated using the methos described here: https://www.nrel.gov/docs/fy15osti/64102.pdf
      Parameters
      ----------
      module :  DataFrame.dtype
          Photovoltaic module, can be parameterized using the method:
            module()
      T_amb:  DataFrame.series
          Dataframe with the temperatures. Can be retrieved using PVGIS
      Irradiance:
          Dataframe with the Irradiance on the photovoltaic surface. Can be retrieved using PVGIS
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
      temp:bool, default=False
          Setting this to True will add an extra column to the output (the temperature column)
      isolated_module:bool, default=False
          Setting this to True will add an extra column to the output, as if the system were to be run only using one module.
          This is not affected by the inverter efficiency. (AC == DC)
      wind:bool, default=False
          Setting this to True will include wind cooling effects on the module.
          wind_speed has to be provided (dataframe)
      wind_speed :  DataFrame.dtype
          Dataframe that includes the wind speed.
      """

      dc_prod = System().dc_production(module=module, T_amb=T_amb, Irradiance = Irradiance,temp=temp, isolated_module=isolated_module ,dc_losses=dc_losses, wind=wind, wind_speed=wind_speed)
      pac_grid_injected = System()._ac_production_inverter(inverter, dc_prod['U (V)'], dc_prod['DC Power']) * (1 - ac_losses)
      pac_grid_injected[pac_grid_injected < 0] = 0
      pac_grid_injected = pac_grid_injected.to_frame()
      pac_grid_injected.columns = ['AC Power']
      pac_grid_injected['DC Power'] = dc_prod['DC Power']
      if wind == True:
        pac_grid_injected['Wind Speed'] = wind_speed
      if temp == True:
        pac_grid_injected['Cell Temperature'] = dc_prod['Cell Temperature']
      if isolated_module == True:
        pac_grid_injected['1 Module AC'] = pac_grid_injected['AC Power'] / (module['modules_per_string']*module['number_of_strings'])
        pac_grid_injected['1 Module DC'] = pac_grid_injected['DC Power'] / (module['modules_per_string']*module['number_of_strings'])

  
      return pac_grid_injected


