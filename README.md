## Defining the location 

```python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS

>>> Location = Location()
>>> location = Location.set_location('Lisbon')

>>> print(location.get_info())

{
 'Address': 'Lisboa, Portugal', 
 'Latitude': 38.7077507, 
 'Longitude': -9.1365919, 
 'Elevation': 10.93380069732666, 
 'Timezone': 'Europe/Lisbon'
 }


```

## Retrieving Hourly data from PVGIS

```python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS

>>> Location = Location()
>>> location = Location.set_location('Lisbon')

>>> PVGIS = PVGIS()
>>> input, output, meta = PVGIS.retrieve_hourly(
                                            latitude=location.latitude, 
                                            longitude=location.longitude
                                            )
>>> print(output)

                     G(i)  H_sun    T2m  WS10m  Int
time                                               
2005-01-01 00:10:00   0.0    0.0  11.29   3.86  0.0
2005-01-01 01:10:00   0.0    0.0  11.19   4.14  0.0
2005-01-01 02:10:00   0.0    0.0  11.08   4.07  0.0
2005-01-01 03:10:00   0.0    0.0  10.94   3.66  0.0
2005-01-01 04:10:00   0.0    0.0  10.84   3.24  0.0
...                   ...    ...    ...    ...  ...
2020-12-31 19:10:00   0.0    0.0  12.50   8.28  0.0
2020-12-31 20:10:00   0.0    0.0  12.12   8.34  0.0
2020-12-31 21:10:00   0.0    0.0  11.58   8.48  0.0
2020-12-31 22:10:00   0.0    0.0  11.41   8.28  0.0
2020-12-31 23:10:00   0.0    0.0  11.36   8.14  0.0

[140256 rows x 5 columns]
```

## Retrieving daily data from PVGIS (July)

```python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS

>>> Location = Location()
>>> location = Location.set_location('Lisbon')

>>> PVGIS = PVGIS()
>>> input, output, meta = PVGIS.retrieve_daily(
                                           latitude=location.latitude, 
                                           longitude=location.longitude,
                                           month=6
                                           )
>>> print(output)

       month    G(i)   Gb(i)   Gd(i)    T2m
time                                       
00:00      6    0.00    0.00    0.00  17.49
01:00      6    0.00    0.00    0.00  17.35
02:00      6    0.00    0.00    0.00  17.21
03:00      6    0.00    0.00    0.00  17.09
04:00      6    0.00    0.00    0.00  16.98
05:00      6    0.00    0.00    0.00  16.91
06:00      6   88.17   36.65   51.52  16.97
07:00      6  244.22  136.17  108.05  17.53
08:00      6  406.34  251.83  154.51  18.42
09:00      6  560.33  366.56  193.77  19.39
10:00      6  691.23  479.46  211.78  20.29
11:00      6  788.61  558.10  230.51  21.05
12:00      6  869.24  632.05  237.19  21.59
13:00      6  877.81  644.56  233.24  21.88
14:00      6  828.50  609.14  219.36  21.92
15:00      6  738.56  540.56  198.01  21.75
16:00      6  594.07  420.05  174.01  21.38
17:00      6  426.24  280.32  145.91  20.88
18:00      6  244.49  141.33  103.16  20.25
19:00      6   82.36   35.16   47.20  19.45
20:00      6    0.00    0.00    0.00  18.68
21:00      6    0.00    0.00    0.00  18.18
22:00      6    0.00    0.00    0.00  17.90
23:00      6    0.00    0.00    0.00  17.69
```

## Retrieving Monthly data from PVGIS (July)

```python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS

>>> Location = Location()
>>> location = Location.set_location('Lisbon')

>>> PVGIS = PVGIS()
>>> input, output, meta = PVGIS.retrieve_monthly(
                                            latitude = location.latitude,
                                            longitude = location.longitude,
                                            startyear=2020,
                                            endyear=2020
                                            )
>>> print(output)

    year  month  H(h)_m  Hb(n)_m    Kd   T2m
0   2020      1   71.23   107.98  0.42  12.8
1   2020      2   98.98   131.26  0.38  13.8
2   2020      3  147.58   168.06  0.36  13.7
3   2020      4  157.34   145.53  0.42  14.8
4   2020      5  218.93   220.23  0.31  18.1
5   2020      6  231.53   235.23  0.30  18.7
6   2020      7  244.94   261.47  0.26  21.2
7   2020      8  208.59   217.80  0.30  20.6
8   2020      9  159.27   167.80  0.36  20.3
9   2020     10  117.98   143.74  0.39  17.1
10  2020     11   68.78    81.66  0.52  15.4
11  2020     12   63.66    93.93  0.46  12.9

```

# from pvmodule.system import System
## Defining the module setup
```python
>>> from pvmodule.system import System
#if nothing is input, it will consider the default module with its parameters.
>>> system = System()
>>> module = system.module(modules_per_string=3)
>>> print(module)
{
    "name": "LG_Neon_2_ LG350N1C-V5",
    "height": 1.686,
    "length": 1.016,
    "width": 40,
    "pdc": 350,
    "umpp": 35.3,
    "impp": 9.92,
    "uoc": 41.3,
    "isc": 10.61,
    "NOCT": 42,
    "tc_pmax": -0.36,
    "tc_voc": -0.27,
    "tc_isc": 0.03,
    "modules_per_string": 3,
    "number_of_strings": 1,
    "losses": 0,
}
```

## Calculating the DC power generated by the previous module setup.
```python

>>> from pvmodule.pvgis import PVGIS
>>> input, output, metadata = PVGIS().retrieve_daily(
                                                location.latitude, 
                                                location.longitude, 
                                                month=7
                                                )

>>> from pvmodule.system import System
>>> system = System()
>>> system_dc = system.dc_production(module, output['T2m'], output['G(i)'])
>>> print(system_dc)

>>> import matplotlib.pyplot as plt
>>> system_dc.plot()

         DC Power    G(i)      V (U)     I (A)
time                                          
00:00    0.000000    0.00   0.000000  0.000000
01:00    0.000000    0.00   0.000000  0.000000
02:00    0.000000    0.00   0.000000  0.000000
03:00    0.000000    0.00   0.000000  0.000000
04:00    0.000000    0.00   0.000000  0.000000
05:00    0.000000    0.00   0.000000  0.000000
06:00   67.326169   62.96  33.595611  0.668006
07:00  230.488507  219.26  33.025791  2.326349
08:00  404.612107  392.92  32.351774  4.168881
09:00  559.303225  554.33  31.698762  5.881441
10:00  697.667399  705.17  31.082645  7.481854
11:00  806.834702  829.20  30.569521  8.797812
12:00  872.878407  907.01  30.234656  9.623376
13:00  881.502513  918.44  30.153389  9.744648
14:00  844.397024  876.07  30.281072  9.295103
15:00  756.681707  776.12  30.630051  8.234633
16:00  624.646497  629.87  31.156362  6.682921
17:00  456.489476  450.85  31.809882  4.783519
18:00  268.290990  259.17  32.522560  2.749794
19:00   91.263308   86.35  33.204521  0.916173
20:00    0.000000    0.00   0.000000  0.000000
21:00    0.000000    0.00   0.000000  0.000000
22:00    0.000000    0.00   0.000000  0.000000
23:00    0.000000    0.00   0.000000  0.000000
```
![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/dc_power_documentation.png)


## Calculating the AC power generated by the previous module setup.
Using a default CECinverter from an included list.

```python

>>> system = System()
#Wind consideration can be included
#system_ac = system.ac_production(module, output['T2m'], output['G(i)'], inverter, wind=True, wind_speed=output['WS10m'])
#system_dc_wind = system.dc_production(module, output['T2m'], output['G(i)'],wind=True, wind_speed=output['WS10m'], temp=True)

>>> inverter_list = system.list_inverters()
>>> inverter = system.select_inverter('ABB: PVI-3.0-OUTD-S-US-A [240V]')
>>> system_ac = system.ac_production(module, output['T2m'], output['G(i)'], inverter)
 
>>> print(system_ac)
>>> import matplotlib.pyplot as plt
>>> system_ac.plot()

         AC Power    DC Power
time                         
00:00    0.000000    0.000000
01:00    0.000000    0.000000
02:00    0.000000    0.000000
03:00    0.000000    0.000000
04:00    0.000000    0.000000
05:00    0.000000    0.000000
06:00   52.413461   67.326169
07:00  212.138796  230.488507
08:00  382.184273  404.612107
09:00  532.896349  559.303225
10:00  667.417007  697.667399
11:00  773.361940  806.834702
12:00  837.374717  872.878407
13:00  845.728999  881.502513
14:00  809.776551  844.397024
15:00  724.710137  756.681707
16:00  596.458487  624.646497
17:00  432.766025  456.489476
18:00  249.094402  268.290990
19:00   75.872365   91.263308
20:00    0.000000    0.000000
21:00    0.000000    0.000000
22:00    0.000000    0.000000
23:00    0.000000    0.000000
```
![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/ac_power_documentation.png)


```python

>>> from pvmodule.location import Location
>>> from pvmodule.system import System
>>> from pvmodule.simulation import Simulation

>>> location = Location().set_location('Covilhã')

>>> module = System().module()
>>> list_inverter = System().list_inverters()
>>> inverter = System().select_inverter('ABB: PVI-3.0-OUTD-S-US-A [240V]',list_inverter)

>>> output, degradacao = Simulation().simulate_vertical(module, inverter, location, duration=15, startyear=2020)

>>> import matplotlib.pyplot as plt

>>> output = output[output.index.month == 7]
>>> output = output[output.index.day == 7]

>>> fig, ax1 = plt.subplots()
 
>>> ax2 = ax1.twinx()
>>> ax1.plot(output.index, output['AC Power'], 'g-')
>>> ax2.plot(output.index, output['Wind Speed'], '*')
>>> ax1.plot(output.index, output['DC Power'], 'r-')
 
>>> ax1.set_xlabel('Time')
>>> ax1.set_ylabel('AC/DC Power', color='r')
>>> ax2.set_ylabel('Wind speed', color='b')

>>> plt.show()

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/vertical_ac_dc_documentation.png)
