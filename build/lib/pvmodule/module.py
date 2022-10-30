#@title Module class { display-mode: "form" }
class Modules():
    def __init__(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'):
      self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'


    def list_modules(self,wattage:int = None, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'):
      """
      List of modules.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'
          Url to the list of modules. Can also be a .csv file.
      """
      import pandas as pd
      self.url = url
      modules = pd.read_csv(self.url).replace(" ", "")
      if wattage != None:
        modules = modules.loc[modules['Pmax'] == int(wattage)]

      from tabulate import tabulate
      if modules.shape[0] > 1000:
        step = 1000
      else:
        step = modules.shape[0]
      for rows in range(0,modules.shape[0],step-1):
        print(tabulate(modules.head(rows), headers='keys', tablefmt='psql'))
      return modules

    def module(self,model:str ,modules_per_string:int=1, number_of_strings:int=1,losses:float=0, first_year_degradation:float=2,annual_degradation:float=0.33, url: str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv') -> dict:
      """
      This method defines the module used for the calculations.
      The standarts module is the LG_Neon_2_ LG350N1C-V5 with the following specsheet:
      """

      import pandas as pd
      module = pd.read_csv(self.url).replace(" ", "")
    
      module = module.loc[module['Model Number'] == model]
      module = module.values.tolist()

      return      {'name': module[0][0]+' '+module[0][1],
                  'height': module[0][19],
                  'length': module[0][18],
                  'pdc': module[0][3],
                  'uoc': module[0][11],
                  'isc': module[0][10],
                  'NOCT': module[0][14],
                  'tc_pmax': module[0][15],
                  'tc_voc': module[0][17],
                  'tc_isc': module[0][16],
                  'modules_per_string': modules_per_string,
                  'number_of_strings': number_of_strings,
                  'losses': losses,
                  'first_year_degradation': first_year_degradation,
                  'annual_degradation': annual_degradation }
      
  