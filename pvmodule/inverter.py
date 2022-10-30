#@title Inverters class { display-mode: "form" }
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

    def list_inverters(self,url:str='https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'):
      """
      List of inverters provided by CEC.
      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      """
      import pandas as pd
      self.url = url
      inverters = pd.read_csv(url).replace(" ", "")

      return inverters
