#@title FINAL (TESE) - Front & Rear Irradiance class { display-mode: "form" }
class Irradiance():
  def __init__(self, url:str="https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/Albedo.csv"):
    self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/Albedo.csv'

  def _get_TMY(self, location, panel_tilt:float, azimuth:float):

    """
    This method gets from PVGIS the necessary data using the TMY.

    Parameters
      ----------
      location
          The location in which the modules will be installed (using the Location() module)
      panel_tilt: float
          The angle in degrees of the modules has with the horizon
      azimuth: float
          The angle the module has with South (South=0º, North = 180º, West = +90º and East = -90º)
      """

    import math
    from datetime import datetime, date, timedelta
    import pandas as pd
    import numpy as np
    from pvmodule import PVGIS

    #params

    #T2m: 2-m air temperature (degree Celsius)
    #RH: relative humidity (%)
    #G(h): Global irradiance on the horizontal plane (W/m2)
    #Gb(n): Beam/direct irradiance on a plane always normal to sun rays (W/m2)
    #Gd(h): Diffuse irradiance on the horizontal plane (W/m2)
    #IR(h): Surface infrared (thermal) irradiance on a horizontal plane (W/m2)
    #WS10m: 10-m total wind speed (m/s)
    #WD10m: 10-m wind direction (0 = N
    #SP: Surface (air) pressure (Pa)

    inputs ,data, metadata = PVGIS().retrieve_tmy(location.latitude,location.longitude)



    data.rename(columns = {'G(h)':'GHI',
                           'Gd(h)':'DHI',
                           'Gb(n)':'DNI',
                           'RH':'Relative Humidity',
                           'T2m':'2m Air Temperature',
                           'WS10m':'10m Wind speed',
                           'WD10m':'10m wind direction',
                           'SP':'Air pressure',
                          }, inplace = True)

  
    data['Time_H'] = data.index.strftime("%H").astype(float)
    data['Time_M'] = data.index.strftime("%M").astype(float)
    data['Time_S'] = data.index.strftime("%S").astype(float)
    data['Month'] = data.index.strftime("%m").astype(float)
    data['Day'] = data.index.strftime("%d").astype(float)


    new_index = data.index.map(lambda t: t.replace(year=2030))
    data=data.set_index(new_index)




    df_both = pd.date_range("2030-01-01 00:00:00", "2030-12-31 23:00:00", freq='5T').to_frame()
    df_both = df_both.drop([0], axis=1)
    df_both = df_both.merge(data, left_index=True, right_index=True, how='left')

    df_both['Month']= df_both['Month'].fillna(method='ffill')
    df_both['Day']= df_both['Day'].fillna(method='ffill')

    data = df_both.interpolate(method='polynomial', order=2)


    DOY =  pd.DatetimeIndex(data.index.values).day_of_year
    data['Declination'] = (23.45*np.sin(np.deg2rad((360/365)*(284+DOY)))).values

    omega = 0.25*(data['Time_H']*60+data['Time_M']+data['Time_S']/60-12*60)
    data = data.drop(['Time_H', 'Time_M','Time_S'], axis=1)

    data['Hour angle'] = omega

    psi = np.arccos(math.sin(np.deg2rad(location.latitude))*np.sin(np.deg2rad(data['Declination']))+math.cos(np.deg2rad(location.latitude))*np.cos(np.deg2rad(data['Declination']))*np.cos(np.deg2rad(omega)))*180/math.pi

    cos_psi = math.sin(np.deg2rad(location.latitude))*np.sin(np.deg2rad(data['Declination']))+math.cos(np.deg2rad(location.latitude))*np.cos(np.deg2rad(data['Declination']))*np.cos(np.deg2rad(omega))

    Zs = azimuth

    lat_rad = np.deg2rad(location.latitude)
    declination_rad = np.deg2rad(data['Declination'])
    panel_tilt_rad = np.deg2rad(panel_tilt)
    Zs_rad = np.deg2rad(Zs)
    Hour_angle_rad = np.deg2rad(data['Hour angle'])

    cos_phi = np.sin(lat_rad)*np.sin(declination_rad)*np.cos(panel_tilt_rad) - np.cos(lat_rad)*np.sin(declination_rad)*np.sin(panel_tilt_rad)*np.cos(Zs_rad) +\
              np.cos(lat_rad)*np.cos(declination_rad)*np.cos(Hour_angle_rad)*np.cos(panel_tilt_rad) +\
              np.sin(lat_rad)*np.cos(declination_rad)*np.cos(Hour_angle_rad)*np.sin(panel_tilt_rad)*np.cos(Zs_rad) +\
              np.cos(declination_rad)*np.sin(Hour_angle_rad)*np.sin(panel_tilt_rad)*np.sin(Zs_rad)


    data['Rb_front'] = abs(np.where( ((azimuth - 90) <= data['Hour angle']) & (data['Hour angle'] <= (azimuth + 90)), cos_phi/cos_psi, 0))
    data['Rb_rear'] = abs(np.where( (data['Hour angle']< (azimuth - 90)) | (data['Hour angle'] > (azimuth + 90)), cos_phi/cos_psi, 0))



    cols = ['Rb_front', 'Rb_rear']
    data[cols] = data[cols].clip(upper=5)

    data['DOY'] = DOY
    data['Solar Zenith angle'] = psi
    data = data.fillna(0)
    

    return inputs ,data, metadata











  def irradiance(self, module, location, panel_tilt:float=35, albedo:float=0.2, azimuth:float = 0, Elevation=2, panel_distance:float = None):

    inputs ,data, metadata = Irradiance()._get_TMY(location, panel_tilt, azimuth)


    if panel_distance == None:
      panel_distance = Irradiance()._modules_spacing(module, panel_tilt, data['DOY'], location.latitude)

    GF_beam = Irradiance()._GF_beam(data)
    GF_diffuse =  Irradiance()._GF_diffuse(data, module, panel_distance, panel_tilt)
    GF_reflected = Irradiance()._GF_reflected(data, albedo, module, panel_distance, panel_tilt, azimuth,Elevation)
    G_front = GF_beam + GF_diffuse + GF_reflected
    data['G_Front'] = G_front

    if module['BIPV'] == 'N' :
      data['Total_G'] = G_front
      data[['GHI', 'DHI','DNI','G_Front','Total_G']] = data[['GHI', 'DHI','DNI','G_Front','Total_G']].clip(lower=0)

      return inputs ,data, metadata


    GR_beam = Irradiance()._GR_beam(data)
    GR_diffuse =  Irradiance()._GR_diffuse(data, module, panel_distance, panel_tilt)
    GR_reflected = Irradiance()._GR_reflected(data, albedo, module, panel_distance, panel_tilt, azimuth,Elevation)

    G_Rear = GR_beam + GR_diffuse + GR_reflected
    data['G_Rear'] = G_Rear
    data['Total_G'] = G_Rear + G_front
    data[['GHI', 'DHI','DNI','G_Front','Total_G','G_Rear']] = data[['GHI', 'DHI','DNI','G_Front','Total_G','G_Rear']].clip(lower=0)


    return inputs ,data, metadata






#
#  FRONT SIDE
#


  def _VF_front_Module2Sky(self, module, panel_distance, panel_tilt):
    import math

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    VF_Module2Sky = H + math.sqrt((A*math.sin(miu*math.pi/180) - H*math.sin(beta*math.pi/180))**2 + (D+H*math.cos(beta*math.pi/180))**2)-math.sqrt((A*math.sin(miu*math.pi/180))**2+D**2)
    VF_Module2Sky = VF_Module2Sky/(2*H)

    return VF_Module2Sky



  def _VF_front_Module2usGround(self, data, module, panel_distance, panel_tilt, azimuth, Elevation):
    import math
    import numpy as np
    import pandas as pd

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    E = Elevation #(Elevação da altura mais baixa do modulo)


    #--- https://arxiv.org/ftp/arxiv/papers/1812/1812.07849.pdf
    gamma = azimuth + 180
    Hour_angle_rad = np.deg2rad(data['Hour angle']) # h em rad
    declination_rad = np.deg2rad(data['Declination']) # delta em rad
    Solar_Zenith_angle_rad = np.deg2rad(data['Solar Zenith angle']) # 0z em rad
    solar_altitude_rad = 90*np.pi/180-np.arcsin(np.cos(Solar_Zenith_angle_rad)) # solar_altitude em rad



    Shadow = np.tan(solar_altitude_rad)*(E + np.sin(beta*np.pi/180)*H) + np.cos(beta*np.pi/180)*H-np.tan(solar_altitude_rad)*E

    S = np.where( (data['GHI'] > 0 )|( data['DHI'] > 0 )| (data['DNI']> 0), Shadow, 0)


    S = pd.DataFrame(S, columns = ['Shadow'] , index=data.index)

    L1 = A * np.cos(miu*np.pi/180) + D - S
    L2 = np.sqrt((A*np.cos(miu*np.pi/180)+D-S+H*np.cos(beta*np.pi/180))**2+(H*np.sin(beta*np.pi/180))**2)

    VF_Module2usGround = ( H + L1 - L2 ) / (2*H)

    return VF_Module2usGround

  def _VF_front_Module2sGround(self, data, module, panel_distance, panel_tilt, azimuth, Elevation):
    import math
    import numpy as np
    import pandas as pd

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    E = Elevation #(Elevação da altura mais baixa do modulo)


    #--- https://arxiv.org/ftp/arxiv/papers/1812/1812.07849.pdf
    gamma = azimuth + 180
    Hour_angle_rad = np.deg2rad(data['Hour angle']) # h em rad
    declination_rad = np.deg2rad(data['Declination']) # delta em rad
    Solar_Zenith_angle_rad = np.deg2rad(data['Solar Zenith angle']) # 0z em rad
    solar_altitude_rad = 90*np.pi/180-np.arcsin(np.cos(Solar_Zenith_angle_rad)) # solar_altitude em rad



    Shadow = np.tan(solar_altitude_rad)*(E + np.sin(beta*np.pi/180)*H) + np.cos(beta*np.pi/180)*H-np.tan(solar_altitude_rad)*E

    S = np.where( (data['GHI'] > 0 )|( data['DHI'] > 0 )| (data['DNI']> 0), Shadow, 0)


    S = pd.DataFrame(S, columns = ['Shadow'], index=data.index)

    L2 = np.sqrt((A*np.cos(miu*np.pi/180)+D-S+H*np.cos(beta*np.pi/180))**2+(H*np.sin(beta*np.pi/180))**2)
    L3 = A*np.cos(miu*np.pi/180)+D
    L4 = np.sqrt((A*np.cos(miu*np.pi/180)+D+H*np.cos(beta*np.pi/180))**2 + (H*np.sin(beta*np.pi/180))**2)
    L5 = A*np.cos(miu*np.pi/180)+D-S

    _VF_Module2sGround = (L2 + L3 - L4 - L5) / (2 * H)

    return _VF_Module2sGround


  def _GF_beam(self, data):

    GF_beam = (data['GHI'] - data['DHI']) * data['Rb_front']

    return GF_beam

  def _GF_diffuse(self, data, module, panel_distance, panel_tilt):

    GF_diffuse = data['DHI']*Irradiance()._VF_front_Module2Sky(module, panel_distance, panel_tilt)

    return GF_diffuse

  def _GF_reflected(self, data, albedo, module, panel_distance, panel_tilt, azimuth, Elevation):

    #VF_Module2sGround - shaded ground

    #VF_Module2usGround - unshaded ground

    VF_Module2Ground = Irradiance()._VF_front_Module2sGround(data, module, panel_distance, panel_tilt,azimuth,Elevation) + Irradiance()._VF_front_Module2usGround(data, module, panel_distance, panel_tilt,azimuth,Elevation)

    GF_reflected = data['GHI']*albedo*VF_Module2Ground['Shadow']

    return GF_reflected


#
# Rear Side
#



  def _VF_rear_Module2Sky(self, module, panel_distance, panel_tilt):
    import math
    import numpy as np

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    L6 = np.sqrt((D+H+np.cos(beta*np.pi/180))**2+(A*np.sin(miu*np.pi/180)-H*np.sin(beta*np.pi/180))**2)
    L7 = np.sqrt((A*np.cos(beta*np.pi/180)+D+H*np.cos(beta*np.pi/180))**2+(H*np.sin(beta*np.pi/180))**2)
    VF_Module2Sky = A + L6 - L7
    VF_Module2Sky = VF_Module2Sky/(2*A)

    return VF_Module2Sky

  def _VF_rear_Module2usGround(self, data, module, panel_distance, panel_tilt, azimuth, Elevation):
    import math
    import numpy as np
    import pandas as pd

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    E = Elevation #(Elevação da altura mais baixa do modulo)


    #--- https://arxiv.org/ftp/arxiv/papers/1812/1812.07849.pdf
    gamma = azimuth + 180
    Hour_angle_rad = np.deg2rad(data['Hour angle']) # h em rad
    declination_rad = np.deg2rad(data['Declination']) # delta em rad
    Solar_Zenith_angle_rad = np.deg2rad(data['Solar Zenith angle']) # 0z em rad
    solar_altitude_rad = 90*np.pi/180-np.arcsin(np.cos(Solar_Zenith_angle_rad)) # solar_altitude em rad



    Shadow = np.tan(solar_altitude_rad)*(E + np.sin(beta*np.pi/180)*H) + np.cos(beta*np.pi/180)*H-np.tan(solar_altitude_rad)*E

    S = np.where( (data['GHI'] > 0 )|( data['DHI'] > 0 )| (data['DNI']> 0), Shadow, 0)

    S = pd.DataFrame(S, columns = ['Shadow'] , index=data.index)

    L8 = np.sqrt((S - A*np.sin(miu*np.pi/180))**2 + (A*np.sin(miu*np.pi/180))**2)
    L3 = A*np.cos(miu*np.pi/180) + D
    L9 = np.sqrt((A*np.sin(miu*np.pi/180))**2+(D)**2)



    VF_Module2usGround = ( L8 + L3 - L9 - S ) / (2*A)


    return VF_Module2usGround

  def _VF_rear_Module2sGround(self, data, module, panel_distance, panel_tilt, azimuth, Elevation):
    import math
    import numpy as np
    import pandas as pd

    A = float(module['height'])
    H = A
    beta = panel_tilt
    miu = beta
    D = panel_distance

    E = Elevation #(Elevação da altura mais baixa do modulo)


    #--- https://arxiv.org/ftp/arxiv/papers/1812/1812.07849.pdf
    gamma = azimuth + 180
    Hour_angle_rad = np.deg2rad(data['Hour angle']) # h em rad
    declination_rad = np.deg2rad(data['Declination']) # delta em rad
    Solar_Zenith_angle_rad = np.deg2rad(data['Solar Zenith angle']) # 0z em rad
    solar_altitude_rad = 90*np.pi/180-np.arcsin(np.cos(Solar_Zenith_angle_rad)) # solar_altitude em rad



    Shadow = np.tan(solar_altitude_rad)*(E + np.sin(beta*np.pi/180)*H) + np.cos(beta*np.pi/180)*H-np.tan(solar_altitude_rad)*E

    S = np.where( (data['GHI'] > 0 )|( data['DHI'] > 0 )| (data['DNI']> 0), Shadow, 0)


    S = pd.DataFrame(S, columns = ['Shadow'], index=data.index)

    L8 = np.sqrt((S - A*np.sin(miu*np.pi/180))**2 + (A*np.sin(miu*np.pi/180))**2)

    _VF_Module2sGround = (A + S - L8) / (2 * A)

    return _VF_Module2sGround





  def _GR_beam(self, data):

    GR_beam = (data['GHI'] - data['DHI']) * data['Rb_rear']

    return GR_beam


  def _GR_diffuse(self, data, module, panel_distance, panel_tilt):

    GR_diffuse = data['DHI']*Irradiance()._VF_rear_Module2Sky(module, panel_distance, panel_tilt)

    return GR_diffuse

  def _GR_reflected(self, data, albedo, module, panel_distance, panel_tilt, azimuth, Elevation):

    VF_rear_Module2usGround = Irradiance()._VF_rear_Module2usGround(data, module, panel_distance, panel_tilt,azimuth,Elevation)

    VF_rear_Module2sGround = Irradiance()._VF_rear_Module2sGround(data, module, panel_distance, panel_tilt,azimuth,Elevation)

    GR_reflected = data['GHI']*albedo*VF_rear_Module2usGround['Shadow'] + data['DHI']*albedo*VF_rear_Module2sGround['Shadow']

    return GR_reflected





    VF_Module2Ground = Irradiance()._VF_front_Module2sGround(data, module, panel_distance, panel_tilt,azimuth,Elevation) + Irradiance()._VF_front_Module2usGround(data, module, panel_distance, panel_tilt,azimuth,Elevation)

    GF_reflected = data['GHI']*albedo*VF_Module2Ground['Shadow']




#
#Auxiliry methods:
#


  def _modules_spacing(self, module, tilt: float, n_year: int = None, latitude: float = None) -> float:
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
        import numpy as np

        if n_year.empty or latitude == None:
            spacing = round(float(module['height']) * ( math.cos(tilt * math.pi / 180) + (math.sin(tilt * math.pi / 180)) / (math.tan(23.45 * math.pi / 180)) ), 3, )

        else:
            delta = 23.45 * np.sin(((360 / 365) * np.pi / 180) * (n_year+284))
            beta_n = 90 - latitude + delta
            spacing = round( float(module['height']) * ( np.cos(tilt * np.pi / 180) + (np.sin(tilt * np.pi / 180)) / (np.tan(beta_n * np.pi / 180)) ), 3, )

        return max(spacing)

  def list_albedo(self):
    """
    This method returns a list of albedos for specific surfaces.
    """
    import pandas as pd
    from tabulate import tabulate
    albedo_list = pd.read_csv(self.url).replace(" ", "")
    return albedo_list


#location = Location().set_location("Oeiras")
#module = Modules().module('6MN6A270')

#_,data,_ = Irradiance().irradiance(module, location, 35, 0.2)

#display(data.head(24))
#data[['G_Front','G_Rear','Total_G']].max()
#data.to_csv("csv.csv")