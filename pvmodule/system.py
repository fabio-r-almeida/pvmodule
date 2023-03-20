#@title FINAL (TESE) System class { display-mode: "form" }
class System():
    def __init__(self):
      pass


############################################
# DC Power calculation.
    def _Tcell(self, Irradiance,temperature_column_name, wind_speed_column_name, irradiance_column_name ):
        #Kurtz - https://pdf.sciencedirectassets.com/277910/1-s2.0-S1876610213X00104/1-s2.0-S1876610213016044/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQC8KgfYrZdUnt7dMO4KJXbgrhHk5QU4ZYGTevVJaz26vQIhAJWcPNCzwINErnCW8XmhYmmi6h87fdKdQ4c6YCxi4ccRKswECEIQBRoMMDU5MDAzNTQ2ODY1IgwnJmllX8y0kAHLrrAqqQQsVDEGiXuqmbwz1YbBbNgCJwQlcRTRJh13IYb8f4k%2BWOAxjyASlwZ0w1kJX4suaWtUHOfXlskEosm09dh2NX1xNysJ3NwlYMPTHQafDK2%2Fg3g7Zc8DIDw9H2TwqI3kN4rx4YkKb72Rqb9GSIbsfDYtubI%2BACL1ajeIr1idCQ%2F2OefyA%2B%2Fw3siLEthT%2BBnJpYDwc4QqhKG8eewdkJwjvJJyQxnPsFfJf72j0wQcUQ0E6xKju1hFZVgQFXFUDP0onXZJr1w6nYmSJp3phHAuseqKoLWHhCuKy0oVUAxZqT9lkEt6wVWrqPQHJQTUfGU8PlBYKAoMZX457IfHgJU1htpOiEmVBQcnP9uQ%2BKO2sMfEE9JmBZwmMD2XnolOJ2p26%2FgUCwXqbN9EwYBQAYo4SYDLn9n24sVavaMrIf9ZqS5HC34LHNe7tvPcEC0J0mHfhzvzUguT93L0mcBq3nHiEgiTVr5JAgYNIPs0Usuj6ObzpIPzK2dWpOnNcAIfns0PayNSpRcNFGiLvW4tCj0Lfq9fxj21aygbHxeOWIXcu32UvghcQMpOAryMJKDcTaWdBlJNJthX2L5n9epY%2BvuioLVtnYjEyIulokBUWUApz8GJaIX6MFv8kh7iGHiDELEpCLghXBU%2Fo%2F7Kqq3dFiXakWrIFHLFiR%2BPbj3iR%2FikYtt1d1NBXpS4Eb2UWCs0oSPigRzmZooPxSQRVYZzqIEdFfFjKkt%2FmjgjXvzfMJ3X85oGOqgBxHDP1OZMxNmHh8neGyQSrtRnFgRB3I0MArd%2BFFPGdNCy76zqcpGb0FSDGNecPpAdFU8V0x%2FrxWrfuYi3RFi0wEplxj11GkRDnrZhmyTzIXA%2BHDAYhorAVUFLWDMRJ4N0Dune077ee5Abs6qxLp%2FjfG61lEslhUvH4tW3GQTI6VgSqbZXjpvzoRcHnDSmVbZV7vKPpqkT3HbPlrGdGf%2FTtoT6M5WOC%2BKk&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221029T092527Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYW7235T6G%2F20221029%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=9c4646596a060c4f3be2149c2fa429c590dcebc5240246f15d308cdb3384a9cc&hash=802d1c967efca932ba4387d0f917156d45726685192d8dfbc0dcc9187c0ab7aa&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1876610213016044&tid=spdf-cb1126c0-67cf-43ee-97cb-272f614a6620&sid=8be7f42727776347ad1a55b471ecb6d1ac82gxrqb&type=client&ua=4d545307060057000602&rr=761add2fcb2169b9
        #converts the 10m to 2m wind (meter for the height of the panels).
        from math import log, e

        psi1 = -3.47
        psi2 = -0.0594
        delta_t = 3

        wind_speed = Irradiance[wind_speed_column_name]
        T_amb = Irradiance[temperature_column_name]


        wind_speed_2m = wind_speed* (2/10)**0.22
        T_module = T_amb + (Irradiance[irradiance_column_name]) * e** (psi1 + psi2*wind_speed_2m)
        T_cell = T_module + ((Irradiance[irradiance_column_name])/1000) * delta_t

        return T_cell


    def dc_production(self, module, Irradiance, irradiance_column_name, temperature_column_name, wind_speed_column_name):

      #Single Point Power Model
      import pandas as pd
      import math

      T_cell = System()._Tcell(Irradiance,temperature_column_name, wind_speed_column_name , irradiance_column_name)

      FF = (module['pdc'])/(module['uoc']*module['isc'])

      ISC = module['isc']
      VOC = module['uoc'] 

      PV_out_Total = FF * VOC * ISC * (1 + (module['tc_pmax']/100)*(T_cell-25))      

      PV_out_Total = PV_out_Total * Irradiance[irradiance_column_name] / 1000


      #losses
      losses = 1 - module['losses']/100

      PV_out_Total = PV_out_Total * (losses)

      estimated_current_total = ISC# * Irradiance[irradiance_column_name]/1000

      PV_output_total_system = PV_out_Total * (module['number_of_modules'])

      PV_output_total_system = pd.DataFrame(PV_output_total_system)

      PV_output_total_system.columns = ['Total DC Power']

      PV_output_total_system['Total Irradiance'] = Irradiance[irradiance_column_name]

      PV_output_total_system['Total U (V)'] = PV_output_total_system['Total DC Power']/estimated_current_total
      PV_output_total_system['Total I (A)'] = estimated_current_total

      PV_output_total_system['Watt per Watt_peak'] = (PV_out_Total/(module['number_of_modules'])) / module['pdc']

      PV_output_total_system = PV_output_total_system.fillna(0)
      PV_output_total_system['Month'] = Irradiance['month']
      PV_output_total_system['T cell'] = T_cell

      PV_output_total_system = PV_output_total_system.sort_values(['Month', 'time'],ascending = [True, True])

     
      return PV_output_total_system


############################################
# DC Power calculation.
    def ac_production(self, dc_production, inverter):
      ac_production = dc_production
      ac_production['Total DC Power'] = ac_production['Total DC Power']/1000
      
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
      z_min = np.polyfit(x, y_min, 3)
      f_min = np.poly1d(z_min)

      z_nom = np.polyfit(x, y_nom, 3)
      f_nom = np.poly1d(z_nom)

      z_max = np.polyfit(x, y_max, 3)
      f_max = np.poly1d(z_max)

      def test_voltage(voltage):
        difference = abs(voltage - min_voltage)
        eff = f_min(voltage)
        if difference > abs(voltage - nominal_voltage):
          eff = f_nom(voltage)
          difference = abs(voltage - nominal_voltage)
        if difference > abs(voltage - max_voltage):
          eff = f_max(voltage)
        return eff


      ac_production['Efficiency'] = ac_production['Total DC Power'].apply(lambda x: test_voltage(x) )
      ac_production['Total AC Power'] = ac_production['Total DC Power']*ac_production['Efficiency']/100
      ac_production['Watt per Watt_peak AC'] = ac_production['Watt per Watt_peak']*ac_production['Efficiency']/100



      

      return ac_production




