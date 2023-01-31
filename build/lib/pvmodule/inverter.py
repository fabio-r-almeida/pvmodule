#@title FINAL (TESE) Inverters class { display-mode: "form" }
class Inverters():
    def __init__(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'):
      self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'

    def inverter(self,name):
      """
      Select the inverter from a provided list.
      To access the list, please use the method:
        list_inverters()

      Parameters
      ----------
      name : str
          The name of the inverter, as listed on the list.
      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      return inverters.loc[inverters['Name'] == name]

    def list_inverters(self,vac:int=None, pmax:int=None,print_list:bool=False):
      """
      List of inverters provided by CEC.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      vac : str, default = None
        Filters the results that are equal to the AC voltage output

      pmax : int, default = None
        Filters the results that are equal to the Max Power input

      print_list : bool, default = False
        Prints list of inverters

      """
      import pandas as pd
      inverters = pd.read_csv(self.url).replace(" ", "")

      if vac != None:
        inverters = inverters.loc[inverters['Vac'] == int(vac)]
      if pmax != None:
        inverters = inverters.loc[inverters['Paco'] == int(pmax)]
      from tabulate import tabulate
      if print_list:
        print(tabulate(inverters, headers='keys', tablefmt='psql'))

      return inverters

    def auto_select_inverter(self,module):
      import pandas as pd

      number_of_modules = module['modules_per_string'] * module['number_of_strings']
      Paco = number_of_modules * module['pdc']
      Vdcmax = module['modules_per_string'] * module['uoc']
      Idcmax =  module['number_of_strings'] * module['isc']


      inverter_list = Inverters().list_inverters(print_list=False)
      inverter_list = inverter_list.loc[inverter_list['Paco'] >= Paco]
      inverter_list = inverter_list.loc[inverter_list['Paco'] <= Paco*2.5]
      inverter_list = inverter_list.loc[inverter_list['Vdcmax'] >= Vdcmax]
      inverter_list = inverter_list.loc[inverter_list['Mppt_high'] >= Vdcmax]
      inverter_list = inverter_list.loc[inverter_list['Mppt_low'] <= Vdcmax]
      inverter_list = inverter_list.loc[inverter_list['Idcmax'] >= Idcmax]

      inverter = pd.DataFrame(inverter_list)
      

      Pdc_max = inverter['Paco']
      Pdco = inverter['Pdco']
      Vdco = inverter['Vdco']
      C0 = inverter['C0']
      C1 = inverter['C1']
      C2 = inverter['C2']
      C3 = inverter['C3']
      Pso = inverter['Pso']

      A = Pdco * (1 + C1 * (Vdcmax - Vdco))
      B = Pso * (1 + C2 * (Vdcmax - Vdco))
      C = C0 * (1 + C3 * (Vdcmax - Vdco))

      inverter['efficiency'] = (Pdc_max / (A - B) - C * (A - B)) * (Paco - B) + C * (Paco - B)**2

      if len(inverter) > 0:
        index = inverter['efficiency'].idxmax()
        inverter = inverter.drop(['efficiency'], axis=1)
        return  inverter.loc[[index]]

      return pd.DataFrame()


