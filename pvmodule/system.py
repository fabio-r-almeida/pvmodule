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

    def __i_v_curve(self):
      '''not yet funcitonal'''
      import math
      I_0 = 1e-10
      I_l = 0.5
      n = 1
      T = 300
      V = 0.5
      q = 1.602176634e-19
      k=1
      I = I_l - I_0 * (math.e**(q*V)/(n*k*T))
      return I_0 * (math.e**(q*V)/(n*k*T))


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

    def module(
        self,
        name: str = "LG_Neon_2_ LG350N1C-V5",
        height: float = 1.686,
        length: float = 1.016,
        width: float = 40,
        pdc: float = 350,
        umpp: float = 35.3,
        impp: float = 9.92,
        uoc: float = 41.3,
        isc: float = 10.61,
        NOCT: float = 42,
        tc_pmax: float = -0.36,
        tc_voc: float = -0.27,
        tc_isc: float = 0.03,
        modules_per_string:int=1,
        number_of_strings:int=1,
        losses:float=0,
    ) -> dict:
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
        Tc_pmax (%/ºC) : -0.36,
        Tc_voc (%/ºC) : -0.27,
        Tc_isc (%/ºC) : 0.03,
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
      self.tc_pmax = tc_pmax
      self.tc_voc = tc_voc
      self.tc_isc = tc_isc
      self.modules_per_string = modules_per_string
      self.number_of_strings = number_of_strings
      self.losses = losses

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
          'tc_pmax':self.tc_pmax,
          'tc_voc':self.tc_voc,
          'tc_isc':self.tc_isc,
          'modules_per_string':self.modules_per_string,
          'number_of_strings':self.number_of_strings,
          'losses':self.losses}
        

    def __dc_production(self,module, T_amb, Irradiance):
      import pandas as pd
      import math

      T_cell = T_amb + (module['NOCT'] - 20) / 800 * Irradiance
      Pdc_max = module['pdc'] * Irradiance / 1000
      delta_T = T_cell - 25
      PV = Pdc_max * (1 + module['tc_pmax'] / 100 * delta_T)

      self.dc_prod = PV * (module['modules_per_string']*module['number_of_strings'])
      self.dc_prod = pd.DataFrame(self.dc_prod)
      self.dc_prod.columns =['dc_Power']
      self.dc_prod['G(i)'] = Irradiance
  
      return self.dc_prod

    def __dc_production_losses(self):
      
      #producao_dc = __dc_production * (1 - dc_losses)
  
      return None


    def __ac_production_inverter(self):
      #pac_inverter = efficiency * __dc_production_losses
  
      return None

    def __ac_grid_injected(self):
      #pac_grid_injected = pac_inverter * (1 - ac_losses)
  
      return None

