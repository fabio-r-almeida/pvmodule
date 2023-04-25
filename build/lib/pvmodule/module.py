#@title FINAL (TESE) - Module class { display-mode: "form" }
class Modules():
    def __init__(self, url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'):
      self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'


    def list_modules(self,wattage:int = None, BIPV:str = None, print_data = True):
      """
      List of modules.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv'
          Url to the list of modules. Can also be a .csv file.
      wattage : int, default = None
          Filter modules by a desired Wattage
      BIPV : str, default = None, default values allows both bi-facial and mono-facial modules to appear in the list
          Filter modules by bi-facial or monofacial modules
            Bi-facial = 'Y'
            Mono-facial = 'N'

      """
      import pandas as pd
      modules = pd.read_csv(self.url).replace(" ", "")
      if wattage != None:
        modules = modules.loc[modules['Pmax'] == int(wattage)]

      if BIPV != None:
        modules = modules.loc[modules['BIPV'] == str(BIPV)]
      modules = modules.loc[modules['Short Side'] != str('nan')]

      return modules

    def module(self,model:str ,number_of_modules:int=1, modules_per_string:int=1, number_of_strings:int=1,losses:float=0, first_year_degradation:float=2,annual_degradation:float=0.33, url: str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/PV_Modules.csv') -> dict:
      """
      This method defines the module used for the calculations.
      """

      import pandas as pd
      module = pd.read_csv(self.url).replace(" ", "")
      module = module.loc[module['Model Number'] == model]
      module = module.fillna(0)
      module = module.values.tolist()
      efficiency = (module[0][3]/1000) / (module[0][19]*module[0][18])

      return      {'brand': module[0][0],
                   'model': module[0][1],
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
                  'number_of_modules': number_of_modules,
                  'losses': losses,
                  'BIPV': module[0][9],
                  'ISC_rear': module[0][20],
                  'Pmax_rear': module[0][21],
                  'efficiency': efficiency,
                  'first_year_degradation': first_year_degradation,
                  'annual_degradation': annual_degradation }

    def modules_spacing(self, module, tilt: float, n_year: int = None, latitude: float = None) -> float:
        """
        This method calculates the necessary spacing between modules to eliminate shading/parcial shading.
        To calculate the worst-case scenario, use only:
          module - the module object
          tilt - surface tilt of the module (degree)

        To calculate for a specific time of the year, use in addition
          n_year - the day in the year
          latitude - latitude of the system
        """
        import math

        if n_year == None or latitude == None:
            self.spacing = round(module['height'] * ( math.cos(tilt * math.pi / 180) + (math.sin(tilt * math.pi / 180)) / (math.tan(23.45 * math.pi / 180)) ), 3, )

        else:
            delta = 23.45 * math.sin(((360 / 365) * math.pi / 180) * (n_year - 81))
            beta_n = 90 - latitude + delta
            self.spacing = round( module['height'] * ( math.cos(tilt * math.pi / 180) + (math.sin(tilt * math.pi / 180)) / (math.tan(beta_n * math.pi / 180)) ), 3, )
        return self.spacing

