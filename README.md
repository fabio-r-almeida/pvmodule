# PV-Module
---

PV-Module is a Python library which focus is to simulate photovoltaic systems.
This module can simulate both Monofacial & Bifacial modules.

## Installation
---

Use the package manager [pip](https://pypi.org/project/pvmodule) to install foobar.

```bash
pip install pvmodule
```

## Usage
---
### Usage - Location

Using the city name, this method will geolocate its coordinates, elevation, timezone.
To use costum locations, just input the desired parameters and they will overwrite the geolocation.

    Parameters
    ----------
    city: str
      The name of the city in which the system is going to be built.
    latitude: float, default = None,
      A specific latitude to overwrite the automatic search.
    longitude: float, default = None,
      A specific longitude to overwrite the automatic search.
    elevation: float, default = None,
      A specific elevation to overwrite the automatic search.
      This elevation corresponds to how many meters the city is above the sea-level.
    timezone: str, default = None,
      The timezone in which the city is located.
      A specific timezone to overwrite the automatic search.
    name: str, default = None,
      The name of the system. This does not affect anything.

```python
>>> from pvmodule.location import Location

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


### Usage - PV Module Selection
To retrieve a list of 17000+ PV modules the following method can be used with the following parameters.

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
```python
>>> from pvmodule.modules import Modules

>>> Modules = Modules()
>>> module_list = Modules.list_modules()

 	Manufacturer 		Model Number 	Safety Certification 	Pmax 	PTC 	Technology 	A_c 	N_s 	N_p 	BIPV 	Isc 	Voc 	Ipmax 	Vpmax 	NOCT 	Tc_pmax 	Tc_isc 	Tc_voc 	Short Side 	Long Side
0 	Ablytek 			6MN6A270 		UL 1703 				270.0 	242.1 	Mono-c-Si 	1.627 	60.0 	1.0 	N 		9.34 	38.63 	8.81 	30.72 	47.4 	-0.4509 	0.0521 	-0.3137 	0.992 	1.64
1 	Ablytek 			6MN6A275 		UL 1703 				275.0 	246.7 	Mono-c-Si 	1.627 	60.0 	1.0 	N 		9.42 	38.97 	8.88 	30.99 	47.4 	-0.4509 	0.0521 	-0.3137 	0.992 	1.64
2 	Ablytek 			6MN6A280 		UL 1703 				280.0 	251.3 	Mono-c-Si 	1.627 	60.0 	1.0 	N 		9.51 	39.31 	8.96 	31.26 	47.4 	-0.4509 	0.0521 	-0.3137 	0.992 	1.64
3 	Ablytek 			6MN6A285 		UL 1703 				285.0 	256.0 	Mono-c-Si 	1.627 	60.0 	1.0 	N 		9.59 	39.65 	9.04 	31.53 	47.4 	-0.4509 	0.0521 	-0.3137 	0.992 	1.64
4 	Ablytek 			6MN6A290 		UL 1703 				290.0 	260.6 	Mono-c-Si 	1.627 	60.0 	1.0 	N 		9.67 	39.99 	9.12 	31.80 	47.4 	-0.4509 	0.0521 	-0.3137 	0.992 	1.64
... 	... 			... 			... 					... 	... 	... 		... 	... 	... 	... 	... 	... 	... 	... 	... 	... 		... 	... 		... 	...
17706 	Zytech Solar 	ZT300P 			UL 1703 				300.0 	271.2 	Multi-c-Si 	1.931 	72.0 	1.0 	N 		8.71 	45.96 	8.26 	36.32 	46.4 	-0.4308 	0.0483 	-0.3199 	0.990 	1.95
17707 	Zytech Solar 	ZT305P 			UL 1703 				305.0 	275.8 	Multi-c-Si 	1.931 	72.0 	1.0 	N 		8.87 	46.12 	8.36 	36.49 	46.4 	-0.4308 	0.0483 	-0.3199 	0.990 	1.95
17708 	Zytech Solar 	ZT310P 			UL 1703 				310.0 	280.5 	Multi-c-Si 	1.931 	72.0 	1.0 	N 		8.90 	46.28 	8.46 	36.66 	46.4 	-0.4308 	0.0483 	-0.3199 	0.990 	1.95
17709 	Zytech Solar 	ZT315P 			UL 1703 				315.0 	285.1 	Multi-c-Si 	1.931 	72.0 	1.0 	N 		9.01 	46.44 	8.56 	36.81 	46.4 	-0.4308 	0.0483 	-0.3199 	0.990 	1.95
17710 	Zytech Solar 	ZT320P 			UL 1703 				320.0 	289.8 	Multi-c-Si 	1.931 	72.0 	1.0 	N 		9.12 	46.60 	8.66 	37.00 	46.4 	-0.4308 	0.0483 	-0.3199 	0.990 	1.95
```


### Usage - PV Inverter Selection
List of +1400 inverters provided by CEC.

      Parameters
      ----------
      url : str, default = 'https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/CEC%20Inverters.csv'
          Url to the list of inverters. Can also be a .csv file.
      vac : str, default = None
        Filters the results that are equal to the AC voltage output

      pmax : int, default = None
        Filters the results that are equal to the Max Power input

      print_list : bool, default = False
        Prints list of inverters

```python
>>> from pvmodule.inverters import Inverters

>>> Inverters = Inverters()
>>> inverter_list = Inverters.list_inverters()

		Name 												Vac 	Pso 		Paco 		Pdco 		Vdco 	C0 				C1 			C2 			C3 			Pnt 		Vdcmax 	Idcmax 		Mppt_low 	Mppt_high 	CEC_Date 	CEC_hybrid
0 		ABB: PVI-3.0-OUTD-S-US-A [208V] 					208 	18.1674 	3000.0 		3142.30 	310.0 	-8.040000e-06 	-0.000011 	0.000999 	-0.000287 	0.100000 	480.0 	10.13650 	100.0 		480.0 		10/15/2018 		N
1 		ABB: PVI-3.0-OUTD-S-US-A [240V] 					240 	16.8813 	3000.0 		3121.67 	340.0 	-5.700000e-06 	-0.000021 	0.000583 	-0.000712 	0.100000 	480.0 	9.18138 	100.0 		480.0 		10/15/2018 		N
2 		ABB: PVI-3.0-OUTD-S-US-A [277V] 					277 	22.0466 	3000.0 		3106.85 	390.0 	-5.460000e-06 	-0.000033 	-0.000032 	-0.001180 	0.200000 	480.0 	7.96628 	100.0 		480.0 		10/15/2018 		N
3 		ABB: PVI-3.0-OUTD-S-US-Z-A [208V] 					208 	18.1674 	3000.0 		3142.30 	310.0 	-8.040000e-06 	-0.000011 	0.000999 	-0.000287 	0.100000 	480.0 	10.13650 	100.0 		480.0 		10/15/2018 		N
4 		ABB: PVI-3.0-OUTD-S-US-Z-A [240V] 					240 	16.8813 	3000.0 		3121.67 	340.0 	-5.700000e-06 	-0.000021 	0.000583 	-0.000712 	0.100000 	480.0 	9.18138 	100.0 		480.0 		10/15/2018 		N
... 	... 												... 	... 		... 		... 		... 	... 			... 		... 	... 			... 		... 	... 		... 		... 		... 			...			
1415 	Yaskawa Solectria Solar: SGI 750XTM [380V] 			380 	3714.1400 	753200.0 	777216.00 	615.0 	-1.410000e-08 	0.000006 	0.001554 	-0.000272 	122.550000 	820.0 	1263.77000 	545.0 		820.0 		NaN 			N	
1416 	Yaskawa Solectria Solar: XGI 1500-125/125 [600V] 	600 	236.8650 	124618.0 	126553.00 	1050.0 	-4.580000e-08 	0.000012 	0.003275 	0.000547 	3.842105 	1250.0 	120.52600 	860.0 		1250.0 		7/21/2020 		N
1417 	Yaskawa Solectria Solar: XGI 1500-125/150 [600V] 	600 	236.8650 	124618.0 	126553.00 	1050.0 	-4.580000e-08 	0.000012 	0.003275 	0.000547 	3.842105 	1250.0 	120.52600 	860.0 		1250.0 		7/21/2020 		N
1418 	Yaskawa Solectria Solar: XGI 1500-150/166 [600V] 	600 	111.3230 	150000.0 	152458.00 	1100.0 	-3.140000e-08 	0.000014 	0.000113 	-0.000354 	2.750000 	1250.0 	138.59800 	860.0 		1250.0 		7/21/2020 		N
1419 	Yaskawa Solectria Solar: XGI 1500-166/166 [600V] 	600 	253.1140 	165139.0 	167945.00 	1050.0 	-5.060000e-08 	0.000014 	0.003122 	0.000368 	3.842105 	1250.0 	159.94800 	860.0 		1250.0 		7/21/2020 		N
 	
```



# Sample Usages 
---

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





## Versions
---

All notable changes to this project will be documented in this file.

### [0.0.34] - 2023-01-31
### Added
- Added new class to calculare front and rear irradiance.
- Resolved minor bugs.
- Corrected/updated formulas to calculate spacing between modules.




## Contributing
---

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
---

[MIT](https://choosealicense.com/licenses/mit/)

## Copyright
---

Copyright (c), 2023, Fabio Ramalho de Almeida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
