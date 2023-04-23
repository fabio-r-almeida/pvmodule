#@title FINAL (TESE) - Agro_Indicators class { display-mode: "form" }
class Agro_Indicators():
  def __init__(self):
    pass
  def PPFD_DLI(self, location , retrieve_all_year_irradiance):
    #PAR, PPF, PPFD
    import pandas as pd
    import numpy as np
    import statistics

    data = retrieve_all_year_irradiance.copy()

    data.index = pd.to_datetime(data.index).strftime('%H:%M:%S')
    data.index = pd.DatetimeIndex(data.index)
    data['Time_H'] = data.index.strftime("%H").astype(float)
    data['Time_M'] = data.index.strftime("%M").astype(float)
    data['Time_S'] = data.index.strftime("%S").astype(float)

    doy_avg = [17 , 47 , 75 , 105 , 135 , 162 , 198 , 228 , 258 , 288 , 318 , 344]
    data['DOY'] = data['month'].apply(lambda x: doy_avg[int(x)-1])

    #delta
    data['Declination'] = (23.45*np.sin(np.deg2rad((360/365)*(284+data['DOY'])))).values

    #w
    data['omega'] = abs((data['Time_H']*60+data['Time_M']+data['Time_S']/60)/4 - 180)
    #cos_psi 
    cos_psi = np.sin(np.deg2rad(location.latitude))*np.sin(np.deg2rad(data['Declination']))+np.cos(np.deg2rad(location.latitude))*np.cos(np.deg2rad(data['Declination']))*np.cos(np.deg2rad(data['omega']))
    data['Solar Elevation Angle'] = np.rad2deg(np.arcsin(cos_psi))
    data['Solar Elevation Angle'] = data['Solar Elevation Angle'].clip(lower=0)

    data.index = retrieve_all_year_irradiance.index   
    data['Solar Zenith Angle'] = 90 - data['Solar Elevation Angle']
    Gs =  1367
    data['PPFD'] = abs(2681*np.cos(np.deg2rad(data['Solar Zenith Angle']))*(data['Global irradiance on a fixed plane']/Gs))
    data['PPFD'] = data['PPFD'].clip(lower=0)

    PPFD = []
    DLI = []

    for month in range(1,13,1):

      data = data.dropna()
      month_data = data.loc[data['month'] == month]      
      PPFD.append(f'{round(month_data["PPFD"].sum(),2)}')
      DLI.append(f'{round(((statistics.mean(month_data["PPFD"])*24*3600)/1000000),2)}')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
    df = pd.DataFrame(months, columns=['months'])
    df['PPFD'] = PPFD
    df['DLI'] = DLI
    return data, df