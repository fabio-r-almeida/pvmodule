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


    fig, ax = plt.subplots(figsize=(15,7),sharex=True)

    pivot_normal = heatmap_data_normal.pivot(index='Time in hours', columns='Day', values='G(i)')
    sns.heatmap(pivot_normal,ax=ax,cmap="Spectral_r",vmin=0, vmax=1000)
    ax.set_title(f'Heatmap of the yearly irradiance for Lat: {location.latitude } Long: {location.longitude }')
    ax.grid()
    plt.tight_layout()
    fig.savefig('Heatmap.png', facecolor=fig.get_facecolor(), edgecolor='none')
    return data

  def Bifacial_Heatmap(self, location, surface_azimuth:int = 90, year:int=2020): 
    
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


    fig, ax = plt.subplots(figsize=(15,7),sharex=True)

    pivot_normal = heatmap_data_normal.pivot(index='Time in hours', columns='Day', values='G(i)')
    sns.heatmap(pivot_normal,ax=ax,cmap="Spectral_r",vmin=0, vmax=1000)
    ax.set_title(f'Heatmap of the yearly irradiance for Lat: {location.latitude } Long: {location.longitude }')
    ax.grid()
    plt.tight_layout()
    fig.savefig('Bifacial_Heatmap.png', facecolor=fig.get_facecolor(), edgecolor='none')

    return data

  def Comparison(self , location, bifacial_data, normal_data, column_name):
    import numpy as np
    irradiance_1 = bifacial_data
    irradiance_2 = normal_data

    if len(irradiance_1) != len(irradiance_2):
      return print("Dataframes don't have the same length.")

    if ('month' in irradiance_1.columns) and ('month' in irradiance_2.columns):
      irradiance_1 = irradiance_1[['month', column_name]]
      irradiance_2 = irradiance_2[['month', column_name]]

      df1 = irradiance_1[column_name].groupby(irradiance_1['month']).sum()
      df2 = irradiance_2[column_name].groupby(irradiance_2['month']).sum()
      df = df1 - df2
      comparison =  ( df1 / df2) * 100
      comparison = comparison.reset_index()
      comparison[column_name] = np.where((df1 / df2) * 100 >= 100 , (df1 / df2) * 100 - 100 , -(df2 / df1) * 100 + 100)

      comparison.rename({'month': 'Month', column_name: 'Irradiance %'}, axis=1, inplace=True)

    else:
      irradiance_1 = irradiance_1[['time', column_name]]
      irradiance_2 = irradiance_2[['time', column_name]]
      df1 = irradiance_1[column_name].groupby(irradiance_1.index.month).sum()
      df2 = irradiance_2[column_name].groupby(irradiance_2.index.month).sum()
      df = df1 - df2
      comparison =  ( df1 / df2) * 100
      comparison = comparison.reset_index()
      comparison[column_name] = np.where((df1 / df2) * 100 >= 100 , (df1 / df2) * 100 - 100 , - (df2 / df1) * 100 + 100)
      comparison.rename({'time': 'Month', column_name: 'Irradiance %'}, axis=1, inplace=True)


    import calendar
    comparison['Month'] = comparison['Month'].apply(lambda x: calendar.month_abbr[int(x)])
 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(15,7))
    NUM_COLORS = 12
    cm = plt.get_cmap('brg')
    ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    colors =[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
    bars = ax.bar(
        x=comparison['Month'],
        height=comparison['Irradiance %'],
        tick_label=comparison['Month'],
        hatch='//', 
        alpha=0.5,
        color=colors
    )

    # Add text annotations to the top of the bars.
    bar_color = bars[0].get_facecolor()
    i = 0
    list_of_values = []
    for bar in bars:
      list_of_values.append(f'{round(df.iloc[i], 1)} $W/m^2$')
      if bar.get_height() < 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() - 1.5,
            f'{round(bar.get_height(), 1)} %',
            horizontalalignment='center',
            color="red",
            weight='bold'
        )
      else:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f'+{round(bar.get_height(), 1)} %',
            horizontalalignment='center',
            color="green",
            weight='bold'
        )
      i += 1



    # Add labels and a title.
    ax.set_ylabel('Irradiance %', labelpad=15, color='#333333', fontsize= 16)
    ax.set_title(f'Vertical Bifacial versus Tilted Monofacial for Lat:{location.latitude} Long:{location.longitude}', pad=15, color='#333333', fontsize= 16)

    gains = round((irradiance_1[column_name].sum() / irradiance_2[column_name].sum()) * 100 - 100,2) 
    gains_watts = round((irradiance_1[column_name].sum() - irradiance_2[column_name].sum())/1000,2)
    bifacial_energy = round(irradiance_1[column_name].sum()/1000,2)
    monofacial_energy = round(irradiance_2[column_name].sum()/1000,2)

    colwidths = 0.92 * (1/12)
    celltext = [[el] for el in list_of_values]
    the_table = plt.table(cellText=celltext,
                          colLabels=["Irradiance"],
                          rowColours=colors,
                          rowLabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"],
                          loc='right',
                          cellLoc='center',
                          rowLoc = 'center',
                          colColours='white',
                          colWidths=[colwidths for x in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]],
                          bbox=[1.1, 0, 0.25, 1]
                          )
    plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
    plt.xticks(rotation=45)
    the_table.set_fontsize(16)
    the_table.scale(2.88,2.88)

  
    if gains < 0:
      ax.text(0.1, 0.80, f'Total loss of {gains} %\nApproximately of {gains_watts} k$W/m^2$\nBifacial Energy of {bifacial_energy} k$W/m^2$ \nNormal Energy of {monofacial_energy} k$W/m^2$',
        style='italic', bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10}, transform=plt.gcf().transFigure)
    else:
      ax.text(0.1,0.80, f'Total gain of {gains} %\nApproximately of {gains_watts} k$W/m^2$\nBifacial Energy of {bifacial_energy} k$W/m^2$ \nNormal Energy of {monofacial_energy} k$W/m^2$',
        style='italic', bbox={'facecolor': 'green', 'alpha': 0.2, 'pad': 10}, transform=plt.gcf().transFigure)

    fig.tight_layout()
    fig.savefig('Comparison.png', facecolor=fig.get_facecolor(), edgecolor='none')
    return comparison

  

  def Efficiency_curve_of_inverter(self, inverter):
      import pandas as pd
      inverter_efficiency = pd.DataFrame()
      x = [inverter['Power Level 10% (kW)'].values[0] ,inverter['Power Level 20% (kW)'].values[0] ,inverter['Power Level 30% (kW)'].values[0] ,inverter['Power Level 50% (kW)'].values[0] ,inverter['Power Level 75% (kW)'].values[0] ,inverter['Power Level 100% (kW)'].values[0] ]
      y_min = [inverter['Efficiency @Vmin 10% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmin 20% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmin 30% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmin 50% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmin 75% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmin 100% Pwr Lvl (%)'].values[0]]
      y_nom = [inverter['Efficiency @Vnom 10% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vnom 20% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vnom 30% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vnom 50% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vnom 75% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vnom 100% Pwr Lvl (%)'].values[0]]
      y_max = [inverter['Efficiency @Vmax 10% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmax 20% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmax 30% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmax 50% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmax 75% Pwr Lvl (%)'].values[0] ,inverter['Efficiency @Vmax 100% Pwr Lvl (%)'].values[0]]


      voltage_list = []
      min_voltage = inverter['Voltage Minimum (Vdc)'].values[0]
      voltage_list.append(min_voltage)

      nominal_voltage = inverter['Voltage Nominal (Vdc)'].values[0]
      voltage_list.append(nominal_voltage)

      max_voltage = inverter['Voltage Maximum (Vdc)'].values[0]
      voltage_list.append(max_voltage)


      import numpy as np
      import pylab
      z_min = np.polyfit(x, y_min, 4)
      f_min = np.poly1d(z_min)

      z_nom = np.polyfit(x, y_nom, 4)
      f_nom = np.poly1d(z_nom)

      z_max = np.polyfit(x, y_max, 4)
      f_max = np.poly1d(z_max)


      xx = np.linspace(min(x), max(x), 30)
      xxx = np.linspace(min(x), max(x), 30)
      
      import matplotlib.pyplot as plt
      plt.rcParams["figure.figsize"] = (15,9)

      pylab.semilogy(xx, f_min(xx), 'gD--', markerfacecolor='none', label=r'$η_{min} = %sx^4 + %sx^3 + %sx^2 + %sx + %s$' % (str(f_min).splitlines()[1].rsplit('x')[0].replace(" ", "").replace("+", "").replace("-", ""),str(f_min).splitlines()[1].rsplit('x')[1].replace(" ", "").replace("+", "").replace("-", ""),str(f_min).splitlines()[1].rsplit('x')[2].replace(" ", "").replace("+", "").replace("-", ""),str(f_min).splitlines()[1].rsplit('x')[3].replace(" ", "").replace("+", "").replace("-", ""),str(f_min).splitlines()[1].rsplit('x')[4].replace(" ", "").replace("+", "").replace("-", "")))
      pylab.semilogy(xx, f_nom(xx), 'bv--', markerfacecolor='none', label=r'$η_{nom} = %sx^4 + %sx^3 + %sx^2 + %sx + %s$' % (str(f_nom).splitlines()[1].rsplit('x')[0].replace(" ", "").replace("+", "").replace("-", ""),str(f_nom).splitlines()[1].rsplit('x')[1].replace(" ", "").replace("+", "").replace("-", ""),str(f_nom).splitlines()[1].rsplit('x')[2].replace(" ", "").replace("+", "").replace("-", ""),str(f_nom).splitlines()[1].rsplit('x')[3].replace(" ", "").replace("+", "").replace("-", ""),str(f_nom).splitlines()[1].rsplit('x')[4].replace(" ", "").replace("+", "").replace("-", "")))
      pylab.semilogy(xx, f_max(xx), 'ms--', markerfacecolor='none', label=r'$η_{max} = %sx^4 + %sx^3 + %sx^2 + %sx + %s$' % (str(f_max).splitlines()[1].rsplit('x')[0].replace(" ", "").replace("+", "").replace("-", ""),str(f_max).splitlines()[1].rsplit('x')[1].replace(" ", "").replace("+", "").replace("-", ""),str(f_max).splitlines()[1].rsplit('x')[2].replace(" ", "").replace("+", "").replace("-", ""),str(f_max).splitlines()[1].rsplit('x')[3].replace(" ", "").replace("+", "").replace("-", ""),str(f_max).splitlines()[1].rsplit('x')[4].replace(" ", "").replace("+", "").replace("-", "")))

    
      y_tick1 =  list(dict.fromkeys(np.round(f_min(xxx),1)))
      y_tick2 =  list(dict.fromkeys(np.round(f_nom(xxx),1)))
      y_tick3 =  list(dict.fromkeys(np.round(f_max(xxx),1)))
      x_tick =  list(dict.fromkeys(np.round(xxx,2)))

      y_tick = (y_tick1 + y_tick2 + y_tick3)
      y_tick = list(dict.fromkeys(y_tick))
      y_tick1 = list(dict.fromkeys(np.round(y_tick,0)))
      del y_tick[::2]
      y_tick = y_tick1 + y_tick
      y_tick = list(dict.fromkeys(y_tick))

      plt.legend(loc='lower right', frameon=True)
      plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
      plt.xticks(x_tick, x_tick)
      plt.yticks(y_tick, y_tick)

      plt.xticks(rotation=45)
      plt.title(f"Inverter Efficiency", fontsize= 16)
      plt.ylabel('Efficiency (%)', fontsize= 16)
      plt.xlabel('Power (kW)', fontsize= 16)
      plt.show()
      fig.savefig('Efficiency_curve_of_inverter.png', facecolor=fig.get_facecolor(), edgecolor='none')
      return [xx, f_min(xx),f_nom(xx),f_max(xx)]

  def plot_multiple_monthly(self, data_list, column_name):
    
    import matplotlib.pyplot as plt
    import pandas as pd
    pd.options.mode.chained_assignment = None 
    fig, ax = plt.subplots()
    hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
    lines = ['--', '-.', '-', ':']
    NUM_COLORS = len(data_list)
    cm = plt.get_cmap('jet')
    ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    colors_i = 0
    hatches_i = 0
    lines_i = 0
    for data in data_list:

      data = data.dropna()
      import calendar
      data['month'] = data['month'].apply(lambda x: calendar.month_abbr[int(x)])

      data[column_name].plot(figsize=(11.69,8.27), ax=ax, fontsize=10, linestyle = lines[lines_i])
      plt.fill_between(data.index, data[column_name], step="mid",hatch=hatches[hatches_i], alpha=0.2)

      colors_i += 1
      hatches_i += 1
      lines_i += 1
      if lines_i == len(lines):
        lines_i = 0
      if hatches_i == len(hatches):
        hatches_i = 0

    plt.title(f"Average Monthly irradiance - {data['month'].values[0]}", fontsize= 10)
    ax.set_ylabel('$W/m^2$', fontsize= 10)
    ax.set_xlabel('time h', fontsize= 10)
    plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
    plt.xticks(rotation=45)
    fig.savefig('plot_multiple_monthly.png', facecolor=fig.get_facecolor(), edgecolor='none')

  def Bifacial_azimuth_test(self, location):
    print("Warning, this might take a while.")

    import concurrent.futures
    import pandas as pd
    from pvmodule import PVGIS
    x = []
    y = []
    output = pd.DataFrame()
    output["X"] = None
    output["Jan"] = None
    output["Feb"] = None
    output["Mar"] = None
    output["Apr"] = None
    output["May"] = None
    output["Jun"] = None
    output["Jul"] = None
    output["Ago"] = None
    output["Sep"] = None
    output["Oct"] = None
    output["Nov"] = None
    output["Dec"] = None
    simple_list=[]

    


    def load_data(location, panel_azimuth):
      _ , data , _ = PVGIS().retrieve_all_year_bifacial(location, panel_azimuth)
      x = panel_azimuth

      X = x
      Jan = data.loc[data['month'] == 1]['Global irradiance on a fixed plane'].sum()
      Feb = data.loc[data['month'] == 2]['Global irradiance on a fixed plane'].sum()
      Mar = data.loc[data['month'] == 3]['Global irradiance on a fixed plane'].sum()
      Apr = data.loc[data['month'] == 4]['Global irradiance on a fixed plane'].sum()
      May = data.loc[data['month'] == 5]['Global irradiance on a fixed plane'].sum()
      Jun = data.loc[data['month'] == 6]['Global irradiance on a fixed plane'].sum()
      Jul = data.loc[data['month'] == 7]['Global irradiance on a fixed plane'].sum()
      Ago = data.loc[data['month'] == 8]['Global irradiance on a fixed plane'].sum()
      Sep = data.loc[data['month'] == 9]['Global irradiance on a fixed plane'].sum()
      Oct = data.loc[data['month'] == 10]['Global irradiance on a fixed plane'].sum()
      Nov = data.loc[data['month'] == 11]['Global irradiance on a fixed plane'].sum()
      Dec = data.loc[data['month'] == 12]['Global irradiance on a fixed plane'].sum()

      list_of_values = [X,Jan, Feb, Mar, Apr, May, Jun, Jul, Ago, Sep, Oct, Nov, Dec]
      simple_list.append(list_of_values)


    for i in range(-90,90,25):
      PANEL_AZIMUTH = list(range(i, 26 + i,5))
      PANEL_AZIMUTH = [x for x in PANEL_AZIMUTH if x <= 90]
      with concurrent.futures.ThreadPoolExecutor(max_workers=len(PANEL_AZIMUTH)) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data,location, panel_azimuth): panel_azimuth for panel_azimuth in PANEL_AZIMUTH}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  return_output = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                pass

    output = pd.DataFrame(simple_list)
    header = ["X", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
    output = output.set_axis(header, axis=1, inplace=False)
    output = output.sort_values(by=['X'])
    output = output.set_index('X')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    Legenda = []
    NUM_COLORS = len(output.columns)
    cm = plt.get_cmap('jet')
    ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for column in output:

      output[column].plot(figsize=(11.69,8.27), ax=ax, fontsize=10)
      Legenda.append(f"{column}")


    plt.title(f"Average Monthly irradiance for Lat:{location.latitude} Long:{location.longitude}", fontsize= 16)
    ax.legend(Legenda, prop={'size': 16})
    ax.set_ylabel('Irradiance $W/m^2$', fontsize= 16)
    ax.set_xlabel('Azimuth angle (degree)', fontsize= 16)
    plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
    x_tick =  list(dict.fromkeys(range(-90,91,5)))
    plt.xticks(x_tick, x_tick)
    fig.savefig('Bifacial_azimuth_test.png', facecolor=fig.get_facecolor(), edgecolor='none')
    return output



  def azimuth_test(self, location, panel_tilt=35):
    print("Warning, this might take a while.")
    import concurrent.futures
    import pandas as pd
    from pvmodule import PVGIS
    x = []
    y = []
    output = pd.DataFrame()
    output["X"] = None
    output["Jan"] = None
    output["Feb"] = None
    output["Mar"] = None
    output["Apr"] = None
    output["May"] = None
    output["Jun"] = None
    output["Jul"] = None
    output["Ago"] = None
    output["Sep"] = None
    output["Oct"] = None
    output["Nov"] = None
    output["Dec"] = None
    simple_list=[]

    


    def load_data(location, panel_azimuth, panel_tilt=35):
      _ , data , _ = PVGIS().retrieve_all_year(location, azimuth= panel_azimuth,panel_tilt=panel_tilt)
      x = panel_azimuth

      X = x
      Jan = data.loc[data['month'] == 1]['Global irradiance on a fixed plane'].sum()
      Feb = data.loc[data['month'] == 2]['Global irradiance on a fixed plane'].sum()
      Mar = data.loc[data['month'] == 3]['Global irradiance on a fixed plane'].sum()
      Apr = data.loc[data['month'] == 4]['Global irradiance on a fixed plane'].sum()
      May = data.loc[data['month'] == 5]['Global irradiance on a fixed plane'].sum()
      Jun = data.loc[data['month'] == 6]['Global irradiance on a fixed plane'].sum()
      Jul = data.loc[data['month'] == 7]['Global irradiance on a fixed plane'].sum()
      Ago = data.loc[data['month'] == 8]['Global irradiance on a fixed plane'].sum()
      Sep = data.loc[data['month'] == 9]['Global irradiance on a fixed plane'].sum()
      Oct = data.loc[data['month'] == 10]['Global irradiance on a fixed plane'].sum()
      Nov = data.loc[data['month'] == 11]['Global irradiance on a fixed plane'].sum()
      Dec = data.loc[data['month'] == 12]['Global irradiance on a fixed plane'].sum()

      list_of_values = [X,Jan, Feb, Mar, Apr, May, Jun, Jul, Ago, Sep, Oct, Nov, Dec]
      simple_list.append(list_of_values)


    for i in range(-90,90,25):
      PANEL_AZIMUTH = list(range(i, 26 + i,5))
      PANEL_AZIMUTH = [x for x in PANEL_AZIMUTH if x <= 90]
      with concurrent.futures.ThreadPoolExecutor(max_workers=len(PANEL_AZIMUTH)) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data,location, panel_azimuth, panel_tilt): panel_azimuth for panel_azimuth in PANEL_AZIMUTH}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  return_output = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                pass

    output = pd.DataFrame(simple_list)
    header = ["X", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
    output = output.set_axis(header, axis=1, inplace=False)
    output = output.sort_values(by=['X'])
    output = output.set_index('X')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    Legenda = []
    NUM_COLORS = len(output.columns)
    cm = plt.get_cmap('jet')
    ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    for column in output:

      output[column].plot(figsize=(11.69,8.27), ax=ax, fontsize=10)
      Legenda.append(f"{column}")


    plt.title(f"Average Monthly irradiance for Lat:{location.latitude} Long:{location.longitude}", fontsize= 16)
    ax.legend(Legenda, prop={'size': 16})
    ax.set_ylabel('Irradiance $W/m^2$', fontsize= 16)
    ax.set_xlabel('Azimuth angle (degree)', fontsize= 16)
    plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
    x_tick =  list(dict.fromkeys(range(-90,91,5)))
    plt.xticks(x_tick, x_tick)
    fig.savefig('azimuth_test.png', facecolor=fig.get_facecolor(), edgecolor='none')
    return output
  def scatter_map(self):
    
    location = Location().set_location(latitude = 38.6973,longitude = -9.30836)
    _,bi_data,_ = PVGIS().retrieve_all_year_bifacial(location, azimuth = 90)

    dc = System().dc_production(module, bi_data, "Global irradiance on a fixed plane", "2m Air Temperature", "10m Wind speed")
    y = dc['Watt per Watt_peak'].to_list()
    x = dc['Total Irradiance'].to_list()

    z = dc['T cell']

    # Python Program illustrating
    # pyplot.colorbar() method
    import numpy as np
    import matplotlib.pyplot as plt
        

    fig, ax = plt.subplots(figsize=(15,7))

    # scatterplot
    plt.scatter(x, y, c=z, cmap="brg")
    plt.ylabel("Power Output (W)")
    plt.xlabel("Irradiance ($W/m^2$)")
      
    plt.colorbar(label="Temperature (°C)", orientation="vertical")
    plt.show()
    fig.savefig('scatter_map.png', facecolor=fig.get_facecolor(), edgecolor='none')

  def plot_multiple_yearly(self,data_list, column_name):
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    for location, data in data_list:
      pd.options.mode.chained_assignment = None 
      fig, ax = plt.subplots()
      NUM_COLORS = 12
      cm = plt.get_cmap('brg')
      ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
      header = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]

	
      # twin object for two different y-axis on the sample plot
      ax2=ax.twinx()
      # make a plot with different y-axis using second axis object
      ax2.set_ylabel('Temperature $\degree C$', fontsize= 20)


      list_of_values = []
      for month in range(1,13,1):

        data = data.dropna()
        month_data = data.loc[data['month'] == month]      
        month_data[column_name].plot(figsize=(11.69,8.27), ax=ax, fontsize=20, label=header[month-1])
        month_data['2m Air Temperature'].plot(figsize=(11.69,8.27), ax=ax2, fontsize=20, label=header[month-1], marker='*', linestyle='')

        list_of_values.append(f'{round(month_data[column_name].sum(),2)} $W/m^2$')

      colors =[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
      colwidths = 0.92 * (1/12)
      celltext = [[el] for el in list_of_values]

      the_table = plt.table(cellText=celltext,
                            colLabels=["Irradiance"],
                            rowColours=colors,
                            rowLabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"],
                            loc='right',
                            cellLoc='center',
                            rowLoc = 'center',
                            colColours='white',
                            colWidths=[colwidths for x in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]],
                            bbox=[1.2, 0, 0.25, 1]
                            )
      ax.legend(header, prop={'size': 20},loc=2 )
      ax.legend(bbox_to_anchor=(0.1, 1))
      plt.title(f"Yearly irradiance for {location}", fontsize= 20)
      ax.set_ylabel('Irradiance $W/m^2$', fontsize= 20)
      ax.set_xlabel('time in hours', fontsize= 20)
      plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
      plt.xticks(rotation=45)
      the_table.set_fontsize(20)
      the_table.scale(2.88,2.88)

  def plot_power_multiple_yearly(self,data_list, column_name, module):
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    for location, data in data_list:
      pd.options.mode.chained_assignment = None 
      fig, ax = plt.subplots()
      NUM_COLORS = 12
      cm = plt.get_cmap('brg')
      ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
      header = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
      days_in_a_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

      list_of_values = []
      list_of_peak_hours = []
      Total_AC_Power = 0
      Total_DC_Power = 0
      Total_PeakHours_Yearly = 0

      for month in range(1,13,1):

        data = data.dropna()
        month_data = data.loc[data['Month'] == month]      
        month_data[column_name].plot(figsize=(11.69,8.27), ax=ax, fontsize=14, label=header[month-1])
        #month_data['T cell'].plot(figsize=(11.69,8.27), ax=ax2, fontsize=20, label=header[month-1], marker='*', linestyle='')

        Total_power_per_month = 0

        peak_hours = 0
        for index, row in month_data.iterrows():
          Total_power_per_month += row['Total AC Power']*1000*days_in_a_month[month-1]

        for index, row in month_data.iterrows():
          if Total_power_per_month - module['pdc']*days_in_a_month[month-1] > 0:
            Total_power_per_month -= module['pdc']*days_in_a_month[month-1]
            peak_hours += 1
          else:
            peak_hours += Total_power_per_month/(module['pdc']*days_in_a_month[month-1])
            Total_power_per_month = 0

        Total_AC_Power += round(month_data["Total AC Power"].sum()*days_in_a_month[month-1],2)
        Total_DC_Power += round(month_data["Total DC Power"].sum()*days_in_a_month[month-1],2)

        list_of_values.append(f'{round(month_data["Total AC Power"].sum()*days_in_a_month[month-1],2)} $kW$')
        list_of_peak_hours.append(f'{round(peak_hours*days_in_a_month[month-1],2)} hours')
        Total_PeakHours_Yearly += round(peak_hours*days_in_a_month[month-1],2)


      print(f"Location: {location}\n Total_DC_Power per Wp: {Total_DC_Power/module['pdc']}\n Total_AC_Power per Wp: {Total_AC_Power/module['pdc']}\n Efficiency: {Total_AC_Power/Total_DC_Power}\n Total Peak hours per year: {Total_PeakHours_Yearly}")
    
    
      colors =[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
      colwidths = 0.92 * (1/12)
      celltext = [[el] for el in list_of_values]
      celltext2 = [[el] for el in list_of_peak_hours]
      celltext = []
      for i in range(0,len(list_of_values)):
        celltext.append([list_of_values[i],list_of_peak_hours[i]])

      the_table = plt.table(cellText=celltext,
                            colLabels=["AC Power","Peak Hours"],
                            rowColours=colors,
                            rowLabels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"],
                            loc='right',
                            cellLoc='center',
                            rowLoc = 'center',
                            colColours=['white','white'],
                            colWidths=[colwidths for x in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]],
                            bbox=[1.1, 0, 0.25, 1]
                            )
      ax.legend(header, prop={'size': 14},loc=2 )
      ax.legend(bbox_to_anchor=(1, 1))
      plt.title(f"Yearly Power production for {location}", fontsize= 14)
      ax.set_ylabel('Power $W/W_p$', fontsize= 14)
      ax.set_xlabel('time in hours', fontsize= 14)
      plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
      the_table.scale(2.88,2.88)
      the_table.auto_set_font_size(False)
      the_table.set_fontsize(11.5)


      

