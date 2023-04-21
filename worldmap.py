#@title  World Map - 4 Concurrent Locations { display-mode: "form" }
#https://simplemaps.com/data/world-cities
class WorldMap():
  def __init__ (self):
    self.url = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/worldcities.csv'
    
  def get_cities(self):

      import pandas as pd
      cities = pd.read_csv(self.url).replace(" ", "")
      return cities
  def plot(self):
    # Importing libraries
    #!pip install geopandas
    import matplotlib.pyplot as plt
    import pandas as pd
    import geopandas as gpd
    from matplotlib.ticker import EngFormatter, StrMethodFormatter
    from google.colab import drive
    drive.mount('/content/gdrive')

    # Reading cvs file using pandas
    df = pd.read_csv('/content/gdrive/MyDrive/Dissertação/Worldmap.csv', 
                  usecols=['Country', 
                  "City Name", 
                  "Latitude", "Longitude",'Horizontal PV','Vertical PV','Ratio V/H'])
    
    #cleaning up data
    df = df[df['Horizontal PV'] > 0] 
    df = df[df['Vertical PV'] > 0] 
    # From GeoPandas, our world map data
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Creating axes and plotting world map
    fig, ax = plt.subplots(figsize=(12, 6))
    worldmap.plot(color="lightgrey", ax=ax)

    # Plotting our Impact Energy data with a color map
    x = df['Longitude']
    y = df['Latitude']
    z = df['Ratio V/H']
    plt.scatter(x, y, c=z, s=2, alpha=0.6, vmin=df['Ratio V/H'].min(), vmax=df['Ratio V/H'].max(),
                cmap='RdYlGn')
    plt.colorbar(label='Ratio V/H')

    # Creating axis limits and title
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])

    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))


    plt.title("Viability of Vertical Bifacial versus Horizontal Monofacial Photovoltaic")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

  def build_map(self):
    import time
    import pandas as pd
    from datetime import datetime, timedelta
    from IPython.display import clear_output
    file_name = '/content/gdrive/MyDrive/Dissertação/Worldmap.csv'
    from google.colab import drive
    drive.mount('/content/gdrive')
    import multiprocessing

    total_map = pd.DataFrame(columns=['index','Country','City Name','Latitude','Longitude','Horizontal PV','Vertical PV','Ratio V/H'])
    total_result = pd.DataFrame(columns=['index','Country','City Name','Latitude','Longitude','Horizontal PV','Vertical PV','Ratio V/H'])

    df = WorldMap().get_cities()

    from os.path import exists
    file_exists = exists(file_name)
    if file_exists:
      drive_file = pd.read_csv(file_name).replace(" ", "")
      column_headers = list(drive_file.columns.values)
      headers = ['index','Country','City Name','Latitude','Longitude','Horizontal PV','Vertical PV','Ratio V/H']
      drive_file = drive_file[headers]
      already_calculated_cities = drive_file['City Name']
      print(f'Done: {len(drive_file)}\nTotal: {len(df)}\n Progress: {(len(drive_file)/len(df))*100} %')
      df = df[~df['City Name'].isin(already_calculated_cities)]
      total_map = drive_file

    import concurrent.futures
    total_time = 0
    total_iters = 0

    NUMBER_OF_CONCURRENT_LOCATIONS = 4
    pool = multiprocessing.Pool(processes=NUMBER_OF_CONCURRENT_LOCATIONS)
    global load_data
    for index, rows in df.groupby(df.index // NUMBER_OF_CONCURRENT_LOCATIONS):
      if len(rows) == NUMBER_OF_CONCURRENT_LOCATIONS:

        t1 = time.time()
        inputs = [rows.iloc[0],rows.iloc[1],rows.iloc[2],rows.iloc[3]]
       
        def load_data(row):
            City_Name = row['City Name']
            Latitude = row['Latitude']
            Longitude = row['Longitude']
            Country = row['Country']
            index = 0

            location = Location().set_location(latitude = Latitude, longitude = Longitude)
            try:
              if Latitude < 0:
                azimuth = 180
              else:
                azimuth = 0
              _,data_horizontal,_ = PVGIS().retrieve_all_year(location, panel_tilt = 'Optimal', azimuth=azimuth)
              Horizontal_PV = data_horizontal['Global irradiance on a fixed plane'].sum()
            except:
                Horizontal_PV = 0

            try:
              _,data_bifacial,_ = PVGIS().retrieve_all_year_bifacial(location, azimuth=90)
              Vertical_PV = data_bifacial['Global irradiance on a fixed plane'].sum()
            except:
              Vertical_PV = 0

            if Horizontal_PV <= 0 or Vertical_PV <= 0:
              Ratio = 0
            else:
              Ratio = Vertical_PV/Horizontal_PV

            result = {'index':index,'Country': Country, 'City Name': City_Name, 'Latitude': Latitude, 'Longitude': Longitude, 'Horizontal PV': Horizontal_PV, 'Vertical PV': Vertical_PV, 'Ratio V/H':Ratio }
            result  = pd.DataFrame([result], columns=result.keys())
            return result

        outputs = pool.map(load_data, inputs)
        outputs.append(total_map)
        total_map = pd.concat(outputs)
        total_time += round(time.time() - t1,2)
        total_iters += 1
        clear_output()
        print(f'Average time of {total_time/total_iters}')
        total_map.to_csv(file_name)
        now = datetime.now()
        current_time = '{:%H:%M:%S}'.format(datetime.now() + timedelta(hours=1))
        print("Current Time =", current_time)

WorldMap().build_map()