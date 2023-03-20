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

## Retrieving daily data from a specific month

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

## Retrieving Bifacial data

```python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS

>>> Location = Location()
>>> location = Location.set_location('Lisbon')

>>> PVGIS = PVGIS()
>>> _,bifacial_data,_ = PVGIS().retrieve_all_year_bifacial(
                                                            location,
                                                            azimuth=90
                                                            )
>>> print(bifacial_data)

Global irradiance on a fixed plane 	Global irradiance on 2-axis tracking plane 	Direct irradiance on a fixed plane 	Direct normal irradiance 	Diffuse irradiance on a fixed plane 	Diffuse irradiance on 2-axis tracking plane 	2m Air Temperature 	10m Wind speed 	month
time 									
00:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	11.29 	2.978333 	1.0
01:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	11.17 	2.827083 	1.0
02:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	10.90 	2.719583 	1.0
03:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	10.73 	2.658750 	1.0
04:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	10.61 	2.638333 	1.0
... 	... 	... 	... 	... 	... 	... 	... 	... 	...
19:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	13.25 	2.841250 	12.0
20:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	12.71 	2.850000 	12.0
21:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	12.61 	2.858333 	12.0
22:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	12.26 	2.861250 	12.0
23:00 	0.0 	0.0 	0.0 	0.0 	0.0 	0.0 	12.17 	2.870000 	12.0

288 rows × 9 columns

```

## Retrieving Monthly data

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

# from pvmodule.graph import Graph

## Yearly irradiance distribuition

``` python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS
>>> from pvmodule.graph import Graph

>>> location = Location().set_location(
                                  latitude = 38.6973, 
                                  longitude = -9.30836
                                  )
>>> _,normal_data,_ = PVGIS().retrieve_all_year(
                                            location, 
                                            panel_tilt=35, 
                                            azimuth=0
                                            )
>>> _,bifacial_data,_ = PVGIS().retrieve_all_year_bifacial(
                                                      location, 
                                                      azimuth=90
                                                      )
>>> Graph().Comparison(
                  normal_data, 
                  bifacial_data, 
                  'Global irradiance on a fixed plane'
                  )
```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/1.png)

``` python
>>> from pvmodule.location import Location
>>> from pvmodule.graph import Graph

>>> location = Location().set_location(latitude = 38.6973,
                                   longitude = -9.30836
                                   )
>>> Graph().Heatmap(
              location, 
              panel_tilt=35, 
              surface_azimuth=0, 
              year=2020
              )
```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/2.png)

## Comparison of monthly average irradiance from vertical vs. 35 horizontal configurations

``` python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS
>>> from pvmodule.graph import Graph

>>> _,bi_data,_ = PVGIS().retrieve_all_year_bifacial(
                                                    location,
                                                    azimuth = 90)
>>> _,normal_data,_ = PVGIS().retrieve_all_year(
                                                location, 
                                                panel_tilt = 35, 
                                                azimuth=0)
>>> Graph().plot_multiple(
                        [bi_data.where(bi_data["month"]==7), normal_data.where(normal_data["month"]==7)],
                        'Global irradiance on a fixed plane'
                        )

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/3.png)


## Irradiance dependancy due to the changes of azimuth
``` python
>>> from pvmodule.location import Location
>>> from pvmodule.graph import Graph

>>> Graph().azimuth_test(location)

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/4.png)

``` python
>>> from pvmodule.location import Location
>>> from pvmodule.graph import Graph

>>> Graph().Bifacial_azimuth_test(location)

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/5.png)


## Maximum, Nominal and Minimum efficiencies of an specified inverter
``` python
>>> from pvmodule.module import Modules
>>> from pvmodule.inverter import Inverters
>>> from pvmodule.graph import Graph

>>> module = Modules().module(
                              'Bi_LG405N2T-L5',
                              losses=5,
                              number_of_modules=20
                              )
>>> inverter, module = Inverters().auto_select_inverter(module)
>>> Graph().Efficiency_curve_of_inverter(inverter)

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/6.png)

## Yearly irradiance curves (of multiple locations)
``` python
>>> from pvmodule.location import Location
>>> from pvmodule.pvgis import PVGIS
>>> from pvmodule.graph import Graph

>>> location = Location().set_location(
                                      latitude = 64.14466555827349,
                                      longitude = -21.95256166366471
                                      )
>>> _,location1,_ = PVGIS().retrieve_all_year(
                                              location,
                                              panel_tilt = 35,
                                              azimuth=0
                                              )

>>> location = Location().set_location(
                                      latitude = 1.3490983309841909,
                                      longitude = 103.80140706509002
                                      )
>>> _,location2,_ = PVGIS().retrieve_all_year(
                                              location,
                                              panel_tilt = 35,
                                              azimuth=0
                                              )

>>> location = Location().set_location(
                                        latitude = 38.6973,
                                        longitude = -9.30836
                                        )
>>> _,location3,_ = PVGIS().retrieve_all_year(
                                              location,
                                              panel_tilt = 35,
                                              azimuth=0
                                              )

>>> Graph().plot_multiple_yearly(
                                [
                                  ('Reykjavik, Iceland',location1)
                                ],
                                'Global irradiance on a fixed plane'
                                )

#>>> Graph().plot_multiple_yearly(
#                                [
#                                  ('Reykjavik, Iceland',location1),
#                                  ('Singapore, Singapore',location2), 
#                                  ('Lisbon, Portugal',location3)
#                                ],
#                                'Global irradiance on a fixed plane'
#                                )

```

![alt text](https://raw.githubusercontent.com/fabio-r-almeida/pvmodule/main/documentation/7.png)



## TODO
---
- Create a simulation method, in which:
  - Calculate pv production
  - Estimate output energy
- ~~Create annual heatmap~~
- ~~Average Irradiance dependancy due to the changes of azimuth~~
- ~~Inverter efficiencies curves~~


## Versions
---

All notable changes to this project will be documented in this file.

### [0.0.66] to [0.0.130] - 2023-03-20
### Added
- Added new *Graph* class.
- Multithreading yearly horizontal and vertical data acquisition with 
  - *PVGIS().retrieve_all_year_bifacial()*
  - *PVGIS().retrieve_all_year()*
### Fixed
- Improved inverter auto-selection.
- Added error exception in both *Inverter* and *PVGIS* class.
### Removed
- Irradiance class will soon be removed due to incorrect irradiance estimations.
  - This issue is believed to be cause due to the incorrect shadow calculation of the module.


### [0.0.62] to [0.0.65] - 2023-03-04
### Added
- Added a second order spline in order to smoothen out the values from PVGIS.
- Changed the timeframe from 1 hour to 5 minutes.
- Change TMY dates for future 2030 dates.



### [0.0.44] to [0.0.61] - 2023-03-04
### Fixed
- Solved issue where Irradiance calculations could be divided by zero and thus creating unlimited irradiance reaching the PV modules.
- Updated the CEC_Inverters database by adding: 
  - Short circuit currents per inverter;
  - Number of MPPT strings per inverter.
- Bug fixing.


### [0.0.35] to [0.0.43] - 2023-02-28
### Added
- Added reverse Geolocalization using coordinates to determine the address.
### Fixed
- Bug fixing.
### Removed
- Removed Timezone from Location class due to unknown issues.


### [0.0.34] - 2023-01-31
### Added
- Added new class to calculare front and rear irradiance.
### Fixed
- Corrected/updated formulas to calculate spacing between modules.
- Resolved minor bugs.





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
