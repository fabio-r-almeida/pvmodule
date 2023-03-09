#@title FINAL (TESE) System class { display-mode: "form" }
class System():
    def __init__(self):
      pass


############################################
# DC Power calculation.
    def _Tcell(self, Irradiance):
        #Kurtz - https://pdf.sciencedirectassets.com/277910/1-s2.0-S1876610213X00104/1-s2.0-S1876610213016044/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQC8KgfYrZdUnt7dMO4KJXbgrhHk5QU4ZYGTevVJaz26vQIhAJWcPNCzwINErnCW8XmhYmmi6h87fdKdQ4c6YCxi4ccRKswECEIQBRoMMDU5MDAzNTQ2ODY1IgwnJmllX8y0kAHLrrAqqQQsVDEGiXuqmbwz1YbBbNgCJwQlcRTRJh13IYb8f4k%2BWOAxjyASlwZ0w1kJX4suaWtUHOfXlskEosm09dh2NX1xNysJ3NwlYMPTHQafDK2%2Fg3g7Zc8DIDw9H2TwqI3kN4rx4YkKb72Rqb9GSIbsfDYtubI%2BACL1ajeIr1idCQ%2F2OefyA%2B%2Fw3siLEthT%2BBnJpYDwc4QqhKG8eewdkJwjvJJyQxnPsFfJf72j0wQcUQ0E6xKju1hFZVgQFXFUDP0onXZJr1w6nYmSJp3phHAuseqKoLWHhCuKy0oVUAxZqT9lkEt6wVWrqPQHJQTUfGU8PlBYKAoMZX457IfHgJU1htpOiEmVBQcnP9uQ%2BKO2sMfEE9JmBZwmMD2XnolOJ2p26%2FgUCwXqbN9EwYBQAYo4SYDLn9n24sVavaMrIf9ZqS5HC34LHNe7tvPcEC0J0mHfhzvzUguT93L0mcBq3nHiEgiTVr5JAgYNIPs0Usuj6ObzpIPzK2dWpOnNcAIfns0PayNSpRcNFGiLvW4tCj0Lfq9fxj21aygbHxeOWIXcu32UvghcQMpOAryMJKDcTaWdBlJNJthX2L5n9epY%2BvuioLVtnYjEyIulokBUWUApz8GJaIX6MFv8kh7iGHiDELEpCLghXBU%2Fo%2F7Kqq3dFiXakWrIFHLFiR%2BPbj3iR%2FikYtt1d1NBXpS4Eb2UWCs0oSPigRzmZooPxSQRVYZzqIEdFfFjKkt%2FmjgjXvzfMJ3X85oGOqgBxHDP1OZMxNmHh8neGyQSrtRnFgRB3I0MArd%2BFFPGdNCy76zqcpGb0FSDGNecPpAdFU8V0x%2FrxWrfuYi3RFi0wEplxj11GkRDnrZhmyTzIXA%2BHDAYhorAVUFLWDMRJ4N0Dune077ee5Abs6qxLp%2FjfG61lEslhUvH4tW3GQTI6VgSqbZXjpvzoRcHnDSmVbZV7vKPpqkT3HbPlrGdGf%2FTtoT6M5WOC%2BKk&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221029T092527Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYW7235T6G%2F20221029%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=9c4646596a060c4f3be2149c2fa429c590dcebc5240246f15d308cdb3384a9cc&hash=802d1c967efca932ba4387d0f917156d45726685192d8dfbc0dcc9187c0ab7aa&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1876610213016044&tid=spdf-cb1126c0-67cf-43ee-97cb-272f614a6620&sid=8be7f42727776347ad1a55b471ecb6d1ac82gxrqb&type=client&ua=4d545307060057000602&rr=761add2fcb2169b9
        #converts the 10m to 2m wind (meter for the height of the panels).
        from math import log, e

        psi1 = -3.47
        psi2 = -0.0594
        delta_t = 3

        wind_speed = Irradiance['2m Air Temperature']
        T_amb = Irradiance['10m Wind speed']


        wind_speed_2m = wind_speed* (2/10)**0.22
        T_module = T_amb + (Irradiance['Total_G']) * e** (psi1 + psi2*wind_speed_2m)
        T_cell = T_module + ((Irradiance['Total_G'])/1000) * delta_t

        return T_cell


    def dc_production(self, module, Irradiance):

      #Single Point Power Model
      import pandas as pd
      import math

      T_cell = System()._Tcell(Irradiance)

      FF = (module['pdc']+module['Pmax_rear'])/(module['uoc']*module['isc'])

      Isc_rear = module['ISC_rear']
      Isc_front = module['isc']

      eff_front = module['pdc']/(1000*module['height']*module['length'])*100
      eff_rear = module['Pmax_rear']/(200*module['height']*module['length'])*100

      ISC = Isc_rear + Isc_front #eq(2.38)


      VOC = module['uoc'] #eq(2.39)

      if 'G_Rear' in Irradiance:
        rear_front_ratio = Irradiance['G_Rear'] / Irradiance['G_Front'] #eq(2.40)
      else:
        rear_front_ratio = 0

      Sci_SC = 1 + rear_front_ratio * (Isc_rear/Isc_front) #eq(2.41)

      PV_out_Total = FF * VOC * ISC * (1 + (module['tc_pmax']/100)*(T_cell-25))        #eq(2.42)
      PV_out_Front = FF * VOC * Isc_front * (1 + (module['tc_pmax']/100)*(T_cell-25))  #eq(2.42)
      PV_out_Rear = FF * VOC * Isc_rear * (1 + (module['tc_pmax']/100)*(T_cell-25))    #eq(2.42)


      if Isc_rear != 0:
        PV_out_Total = PV_out_Total * Irradiance['Total_G'] / 1200
        PV_out_Front = PV_out_Front * Irradiance['G_Front'] / 1000
        PV_out_Rear = PV_out_Rear * Irradiance['G_Rear'] / 200
      else: 
        PV_out_Front = PV_out_Front * Irradiance['G_Front'] / 1000
        PV_out_Total = PV_out_Total * Irradiance['Total_G'] / 1000
        PV_out_Rear = 0

      #losses
      losses = 1 - module['losses']/100

      PV_out_Total = PV_out_Total * (losses)
      PV_out_Front = PV_out_Front * (losses)
      PV_out_Rear = PV_out_Rear * (losses)

      estimated_current_total = ISC*Irradiance['Total_G']/1200
      estimated_current_front = Isc_front*Irradiance['G_Front']/1000
      if Isc_rear != 0:
        estimated_current_rear = Isc_rear*Irradiance['G_Rear']/200
      else:
        estimated_current_rear = 0

      PV_output_total_system = PV_out_Total * (module['modules_per_string']*module['number_of_strings'])
      PV_output_front_system = PV_out_Front * (module['modules_per_string']*module['number_of_strings'])
      PV_output_rear_system = PV_out_Rear * (module['modules_per_string']*module['number_of_strings'])

      PV_output_total_system = pd.DataFrame(PV_output_total_system)

      PV_output_total_system.columns = ['Total DC Power']
      PV_output_total_system['Front DC Power'] = PV_output_front_system
      PV_output_total_system['Rear DC Power'] = PV_output_rear_system


      PV_output_total_system['Total Irradiance'] = Irradiance['Total_G']
      PV_output_total_system['Front Irradiance'] = Irradiance['G_Front']

      if Isc_rear != 0:
        PV_output_total_system['Rear Irradiance'] = Irradiance['G_Rear']
      else:
        PV_output_total_system['Rear Irradiance'] = 0


      PV_output_total_system['Total U (V)'] = PV_out_Total/estimated_current_total
      PV_output_total_system['Total I (A)'] = estimated_current_total

      PV_output_total_system['Front U (V)'] = PV_out_Total/estimated_current_front
      PV_output_total_system['Front I (A)'] = estimated_current_front

      if Isc_rear != 0:
        PV_output_total_system['Rear U (V)'] = PV_out_Total/estimated_current_rear
        PV_output_total_system['Rear I (A)'] = estimated_current_rear
      else: 
        PV_output_total_system['Rear U (V)'] = 0
        PV_output_total_system['Rear I (A)'] = 0

      PV_output_total_system['Watt per Watt_peak'] = (PV_out_Total/(module['modules_per_string']*module['number_of_strings'])) / module['pdc']

      PV_output_total_system = PV_output_total_system.fillna(0)
      PV_output_total_system['Time_H'] = Irradiance['Time_H']

     
      return PV_output_total_system


############################################
# DC Power calculation.
    def ac_production(self, dc_production, inverter):
      ac_production = dc_production


      ac_production['Min Usage %'] = ac_production['Total DC Power'] / inverter['Voltage Minimum (Vdc)'] * 100
      ac_production['Nominal Usage %'] = ac_production['Total DC Power'] / inverter['Voltage Nominal (Vdc)'] * 100
      ac_production['Max Usage %'] = ac_production['Total DC Power'] / inverter['Voltage Maximum (Vdc)'] * 100

      return ac_production




