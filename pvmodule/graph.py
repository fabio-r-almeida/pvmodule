#@title FINAL (TESE) Graph { display-mode: "form" }

class Graph():
  def __init__(self):
    pass
  def Heatmap(self, location, panel_tilt:int = 35, surface_azimuth:int = 0, year:int=2020): 
    
    from pvmodule import PVGIS
    import calendar
    import matplotlib.pyplot as plt
    import seaborn as sns

    _, data, _ = PVGIS().retrieve_hourly(location.latitude, location.longitude , startyear = year, endyear= year,surface_tilt = panel_tilt, surface_azimuth = surface_azimuth)

    heatmap_data_normal = data.iloc[-(365 + calendar.isleap(int(2020)))*24:].copy()
    heatmap_data_normal = heatmap_data_normal.drop(columns=['H_sun', 'T2m', 'WS10m', 'Int'], axis=1)
    heatmap_data_normal['Day'] = heatmap_data_normal.index.date
    heatmap_data_normal['Time in hours' ] = heatmap_data_normal.index.time
    heatmap_data_normal = heatmap_data_normal.reset_index(drop=True)


    fig, ax = plt.subplots(figsize=(15,7),sharex=True);

    pivot_normal = heatmap_data_normal.pivot(index='Time in hours', columns='Day', values='G(i)')
    sns.heatmap(pivot_normal,ax=ax,cmap="Spectral_r",vmin=0, vmax=1000)
    ax.set_title(f'Lat: {location.latitude } Long: {location.longitude }');
    ax.grid()
    plt.tight_layout()

  def Bifacial_Heatmap(self, location, surface_azimuth:int = 0, year:int=2020): 
    
    from pvmodule import PVGIS
    import calendar
    import matplotlib.pyplot as plt
    import seaborn as sns

    panel_tilt = 90

    azimuth_backsheet = int(surface_azimuth) + 180
    if azimuth_backsheet <= 180:
      pass
    else:
      azimuth_backsheet = azimuth_backsheet - 360

    _, data1, _ = PVGIS().retrieve_hourly(location.latitude, location.longitude , startyear = year, endyear= year, surface_tilt = panel_tilt, surface_azimuth = surface_azimuth)
    _, data2, _ = PVGIS().retrieve_hourly(location.latitude, location.longitude , startyear = year, endyear= year, surface_tilt = panel_tilt, surface_azimuth = azimuth_backsheet)
    
    data2 = data2.drop(['H_sun','T2m','WS10m'], axis=1)
    data = data1.add(data2, fill_value=0)


    heatmap_data_normal = data.iloc[-(365 + calendar.isleap(int(2020)))*24:].copy()
    heatmap_data_normal = heatmap_data_normal.drop(columns=['H_sun', 'T2m', 'WS10m', 'Int'], axis=1)
    heatmap_data_normal['Day'] = heatmap_data_normal.index.date
    heatmap_data_normal['Time in hours' ] = heatmap_data_normal.index.time
    heatmap_data_normal = heatmap_data_normal.reset_index(drop=True)


    fig, ax = plt.subplots(figsize=(15,7),sharex=True);

    pivot_normal = heatmap_data_normal.pivot(index='Time in hours', columns='Day', values='G(i)')
    sns.heatmap(pivot_normal,ax=ax,cmap="Spectral_r",vmin=0, vmax=1000)
    ax.set_title(f'Lat: {location.latitude } Long: {location.longitude }');
    ax.grid()
    plt.tight_layout()

  def Comparison(self, irradiance_1, irradiance_2, column_name):
    if len(irradiance_1) != len(irradiance_2):
      return print("Dataframes don't have the same length.")

    if ('month' in irradiance_1.columns) and ('month' in irradiance_2.columns):
      df1 = irradiance_1[column_name].groupby(irradiance_1['month']).sum()
      df2 = irradiance_2[column_name].groupby(irradiance_2['month']).sum()
      comparison =  ( (df1 - df2) / df1) * 100
      comparison = comparison.reset_index()
      comparison.rename({'month': 'Month', column_name: 'Irradiance %'}, axis=1, inplace=True)

    else:
      df1 = irradiance_1[column_name].groupby(irradiance_1.index.month).sum()
      df2 = irradiance_2[column_name].groupby(irradiance_2.index.month).sum()
      comparison =  ( (df1 - df2) / df1) * 100
      comparison = comparison.reset_index()
      comparison.rename({'time': 'Month', column_name: 'Irradiance %'}, axis=1, inplace=True)
 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(15,7),sharex=True);
    bars = ax.bar(
        x=comparison['Month'],
        height=comparison['Irradiance %'],
        tick_label=comparison['Month'],
        hatch='//', 
        alpha=0.5, 
        color='#ff4dc4'
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    # Add text annotations to the top of the bars.
    bar_color = bars[0].get_facecolor()
    for bar in bars:
      if bar.get_height() < 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() - 2.5,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color="black",
            weight='bold'
        )
      else:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2.5,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color="black",
            weight='bold'
        )

    # Add labels and a title.
    ax.set_xlabel('Month', labelpad=15, color='#333333')
    ax.set_ylabel('Irradiance %', labelpad=15, color='#333333')
    ax.set_title('Vertical Bifacial versus Tilted Monofacial', pad=15, color='#333333',
                weight='bold')

    fig.tight_layout()

      

    


    





