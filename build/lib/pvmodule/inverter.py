#@title FINAL (TESE) Inverters class { display-mode: "form" }
class Inverters():
    def __init__(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC_Inverters.csv'):
      self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC_Inverters.csv'

    def inverter(self,name):
      """
      Select the inverter from a provided list.
      To access the list, please use the method:
        list_inverters()

      Parameters
      ----------
      name : str
          The Model Number of the inverter, as listed on the list.
      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      return inverters.loc[inverters['Model Number'] == name]

    def list_inverters(self,vac:int=None, pmax:int=None,print_list:bool=False):
      """
      List of inverters provided by CEC.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC_Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      vac : str, default = None
        Filters the results that are equal to the AC voltage output

      pmax : int, default = None
        Filters the results that are equal to the Max Power output

      print_list : bool, default = False
        Prints list of inverters

      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      if vac != None:
        inverters = inverters.loc[inverters['Nominal Voltage (Vac)'] == int(vac)]
      if pmax != None:
        inverters = inverters.loc[inverters['Maximum Continuous Output Power (kW)'] == int(pmax)]

      return inverters



    def auto_select_inverter(self,module):
      import pandas as pd
      number_of_modules = module['number_of_modules']
      Max_Input_DC_Power = number_of_modules * module['pdc'] / 1000
      Vdcmax = module['uoc']
      Idcmax = module['isc']


      inverter_list = Inverters().list_inverters(print_list=False)
      inverter_list = inverter_list.loc[inverter_list['Maximum Continuous Output Power (kW)'] >= Max_Input_DC_Power*0.7]
      inverter_list = inverter_list.loc[inverter_list['Maximum Continuous Output Power (kW)'] <= Max_Input_DC_Power*1.2]
      inverter_list = inverter_list.loc[inverter_list['Maximum Short Circuit Current / String'] >= Idcmax]

      inverter_list = inverter_list.loc[inverter_list['Voltage Maximum (Vdc)'] >= (Vdcmax/inverter_list['Max strings input'])*number_of_modules]
      #inverter_list = inverter_list.loc[inverter_list['Voltage Minimum (Vdc)'] <= Vdcmax]
      inverter_list = inverter_list.sort_values(by='Maximum Continuous Output Power (kW)', ascending=True)

      inverter = pd.DataFrame(inverter_list)
      inverter['efficiency'] = inverter['Weighted Efficiency (%)']
      inverter = inverter.sort_values(by='Maximum Continuous Output Power (kW)', ascending=True)

      if len(inverter) > 0:
        inverter = inverter.drop( inverter.index.to_list()[1:] ,axis = 0 )
        module['modules_per_string'] = round(number_of_modules/inverter['Max strings input'].iloc[0],0)
        module['number_of_strings'] = round(inverter['Max strings input'].iloc[0],0)
        module['number_of_modules'] = module['modules_per_string']*module['number_of_strings']
        return  inverter, module
      return pd.DataFrame(), module
      class NoInverterFound(Exception):
        pass
      raise NoInverterFound("There is no compatible inverter.")



