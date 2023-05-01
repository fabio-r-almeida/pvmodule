#@title FINAL (TESE) PVGIS class { display-mode: "form" }
class PVGIS():
    """
    PVGIS class retrieves real-world data from the PVGIS-API.
    It uses by defaults the version v5_2, if wanted, it can be swapped by changing the url with another version.
    The months count start at January=0 and December=11
    """

    def __init__(self):
        # hourly
        self.latitude = None  # latitude
        self.longitude = None  # longitude
        self.usehorizon = None  # usehorizon
        self.userhorizon = None  # userhorizon
        self.raddatabase = None  # raddatabase
        self.startyear = None  # startyear
        self.endyear = None  # endyear
        self.pvcalculation = None  # pvcalculation
        self.peakpower = None  # peakpower
        self.pvtechchoice = None  # pvtechchoice
        self.mountingplace = None  # mountingplace
        self.loss = None  # loss
        self.trackingtype = None  # trackingtype
        self.surface_tilt = None  # surface_tilt
        self.surface_azimuth = None  # surface_azimuth
        self.optimalinclination = None  # optimalinclination
        self.optimalangles = None  # optimalangles
        self.components = None  # components
        self.outputformat = None  # outputformat
        self.url = None  # url
        self.data = None
        # monthly
        self.horirrad = None  # horirrad
        self.optrad = None  # optrad
        self.selectrad = None  # selectrad
        self.angle = None  # angle
        self.mr_dni = None  # mr_dni
        self.d2g = None  # d2g
        self.avtemp = None  # avtemp
        # daily
        self.month = None  # month
        self.angle = None  # angle
        self.aspect = None  # aspect
        self.global_irr = None  # global_irr
        self.glob_2axis = None  # glob_2axis
        self.clearsky = None  # clearsky
        self.clearsky_2axis = None  # clearsky_2axis
        self.showtemperatures = None  # ,showtemperatures
        self.localtime = None  # localtime

    def retrieve_hourly( self, latitude: float, longitude: float, usehorizon: int = 1, userhorizon: int = None, raddatabase: str = 'PVGIS-ERA5', startyear: int = 2020, endyear: int = 2020, pvcalculation: int = 0, peakpower: float = None, pvtechchoice: str = "crystSi", mountingplace: str = "free", loss: float = None, trackingtype: int = 0, surface_tilt: float = 0, surface_azimuth: float = 0, optimalinclination: int = 0, optimalangles: int = 0, components: int = 0, outputformat: str = "json", url: str = "http://re.jrc.ec.europa.eu/api/v5_2/") -> object:
        """
        Hourly Data: This method retrieves real-world data using the PVGIS-API.
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metedata
        Parameters
        ----------
        latitude: float
          Latitude, in decimal degrees, south is negative.
        longitude: float
          Longitude, in decimal degrees, west is negative.
        usehorizon: int, default = 1,
          Calculate taking into account shadows from high horizon. Value of 1 for "yes".
        userhorizon: int, default = None,
          Height of the horizon at equidistant directions around the point of interest, in degrees. Starting at north and moving clockwise. The series '0,10,20,30,40,15,25,5' would mean the horizon height is 0° due north, 10° for north-east, 20° for east, 30° for south-east, etc.
        raddatabase: str, default = None,
          Name of the radiation database (DB): "PVGIS-SARAH" for Europe, Africa and Asia or "PVGIS-NSRDB" for the Americas between 60°N and 20°S, "PVGIS-ERA5" and "PVGIS-COSMO" for Europe (including high-latitudes), and "PVGIS-CMSAF" for Europe and Africa (will be deprecated). The default DBs are PVGIS-SARAH, PVGIS-NSRDB and PVGIS-ERA5 based on the chosen location.
        startyear: int, default = None,
          First year of the output of hourly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the first year of the DB.
        endyear: int, default = None,
          Final year of the output of hourly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the last year of the DB.
        pvcalculation: int, default = 0,
          If "0" outputs only solar radiation calculations, if "1" outputs the estimation of hourly PV production as well.
        peakpower: float, default = None,
          Nominal power of the PV system, in kW.
        pvtechchoice: str, default = "crystSi",
          PV technology. Choices are: "crystSi", "CIS", "CdTe" and "Unknown".
        mountingplace: str, default = "free",
          Type of mounting of the PV modules. Choices are: "free" for free-standing and "building" for building-integrated.
        loss: float, default = None,
          Sum of system losses, in percent.
        trackingtype: int, default = 0,
          Type of suntracking used, 0=fixed, 1=single horizontal axis aligned north-south, 2=two-axis tracking, 3=vertical axis tracking, 4=single horizontal axis aligned east-west, 5=single inclined axis aligned north-south.
        surface_tilt: float, default = 0,
          Inclination angle from horizontal plane. Not relevant for 2-axis tracking.
        surface_azimuth: float, default = 0,
          Orientation (azimuth) angle of the (fixed) plane, 0=south, 90=west, -90=east. Not relevant for tracking planes.
        optimalinclination: int, default = 0,
          Calculate the optimum inclination angle. Value of 1 for "yes". All other values (or no value) mean "no". Not relevant for 2-axis tracking.
        optimalangles: int, default = 0,
          Calculate the optimum inclination AND orientation angles. Value of 1 for "yes". All other values (or no value) mean "no". Not relevant for tracking planes.
        components: int, default = 0,
          If "1" outputs beam, diffuse and reflected radiation components. Otherwise, it outputs only global values.
        outputformat: str, default = "json",
          Type of output. Choices are: "csv" for the normal csv output with text explanations, "basic" to get only the data output with no text, and "json".
        url: str, default = "http://re.jrc.ec.europa.eu/api/v5_2/",
        """
        import requests
        import pandas as pd

        self.latitude = latitude
        self.longitude = longitude
        self.usehorizon = usehorizon
        self.userhorizon = userhorizon
        self.raddatabase = raddatabase
        self.startyear = startyear
        self.endyear = endyear
        self.pvcalculation = pvcalculation
        self.peakpower = peakpower
        self.pvtechchoice = pvtechchoice
        self.mountingplace = mountingplace
        self.loss = loss
        self.trackingtype = trackingtype
        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth
        self.optimalinclination = optimalinclination
        self.optimalangles = optimalangles
        self.components = components
        self.outputformat = outputformat
        self.url = url
        self.data = None

        url = self.url + f"seriescalc?lat={self.latitude}&lon={self.longitude}"

        if self.usehorizon != None:
            url = url + f"&usehorizon={self.usehorizon}"
        if self.userhorizon != None:
            url = url + f"&userhorizon={self.userhorizon}"
        if self.raddatabase != None:
            url = url + f"&raddatabase={self.raddatabase}"
        if self.startyear != None:
            url = url + f"&startyear={self.startyear}"
        if self.endyear != None:
            url = url + f"&endyear={self.endyear}"
        if self.pvcalculation != None:
            url = url + f"&pvcalculation={self.pvcalculation}"
        if self.peakpower != None:
            url = url + f"&peakpower={self.peakpower}"
        if self.pvtechchoice != None:
            url = url + f"&pvtechchoice={self.pvtechchoice}"
        if self.mountingplace != None:
            url = url + f"&mountingplace={self.mountingplace}"
        if self.loss != None:
            url = url + f"&loss={self.loss}"
        if self.trackingtype != None:
            url = url + f"&trackingtype={self.trackingtype}"
        if self.surface_tilt != None:
            url = url + f"&angle={self.surface_tilt}"
        if self.surface_azimuth != None:
            url = url + f"&aspect={self.surface_azimuth}"
        if self.optimalinclination != None:
            url = url + f"&optimalinclination={self.optimalinclination}"
        if self.optimalangles != None:
            url = url + f"&optimalangles={self.optimalangles}"
        if self.components != None:
            url = url + f"&components={self.components}"
        if self.outputformat != None:
            url = url + f"&outputformat={self.outputformat}"

        self.url = url
        data = requests.get(url).json()
        try:
            outputs = data["outputs"]["hourly"]
            outputs = pd.json_normalize(outputs)
            outputs["time"] = pd.to_datetime(outputs.time, format="%Y%m%d:%H%M")

            outputs = outputs.set_index("time")

            inputs = data["inputs"]

            meta = data["meta"]
        except:
            class FaultyDataInput(Exception):
              pass
            raise FaultyDataInput("Error with the PVGIS input.")

        self.data = inputs, outputs, meta

        if(outputs['T2m'].mean() == 0 or outputs['WS10m'].mean() == 0):
          if 'v5_2' in self.url:
            return PVGIS().retrieve_hourly(self.latitude, self.longitude, self.usehorizon, self.userhorizon, self.raddatabase, self.startyear, self.endyear, self.pvcalculation, self.peakpower, self.pvtechchoice, self.mountingplace, self.loss, self.trackingtype, self.surface_tilt, self.surface_azimuth, self.optimalinclination, self.optimalangles, self.components, self.outputformat, url = "http://re.jrc.ec.europa.eu/api/v5_1/")

        return self.data

    def retrieve_hourly_bifacial( self, latitude: float, longitude: float, usehorizon: int = 1, userhorizon: int = None, raddatabase: str = 'PVGIS-ERA5', startyear: int = 2020, endyear: int = 2020, pvcalculation: int = 0, peakpower: float = None, pvtechchoice: str = "crystSi", mountingplace: str = "free", loss: float = None, trackingtype: int = 0, surface_tilt: float = 0, surface_azimuth: float = 0, optimalinclination: int = 0, optimalangles: int = 0, components: int = 0, outputformat: str = "json", url: str = "http://re.jrc.ec.europa.eu/api/v5_2/") -> object:
        
        panel_tilt = 90
        azimuth_backsheet = int(surface_azimuth) + 180
        if azimuth_backsheet <= 180:
          pass
        else:
          azimuth_backsheet = azimuth_backsheet - 360
          
        _, data1, _ = PVGIS().retrieve_hourly(latitude, longitude , startyear = startyear, endyear= endyear, surface_tilt = surface_tilt, surface_azimuth = surface_azimuth)
        _, data2, _ = PVGIS().retrieve_hourly(latitude, longitude , startyear = startyear, endyear= endyear, surface_tilt = surface_tilt, surface_azimuth = azimuth_backsheet)

        data2 = data2.drop(['H_sun','T2m','WS10m'], axis=1)
        data = data1.add(data2, fill_value=0)
        return data

    def retrieve_monthly(self, latitude: float, longitude: float, usehorizon: int = 1, userhorizon: int = None, raddatabase: str = None, startyear: int = None, endyear: int = None, horirrad: int = 1, optrad: int = 0, selectrad: int = 0, angle: int = 0, mr_dni: int = 1, d2g: int = 1, avtemp: int = 1, outputformat: str = "json", url: str = "http://re.jrc.ec.europa.eu/api/v5_2/", ) -> object:
        """
        Monthly Data: This method retrieves real-world data using the PVGIS-API.
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metadata

        Parameters
        ----------
        latitude: float
          Latitude, in decimal degrees, south is negative.
        longitude: float
          Longitude, in decimal degrees, west is negative.
        usehorizon: int, default = 1,
          Calculate taking into account shadows from high horizon. Value of 1 for "yes".
        userhorizon: int, default = None,
          Height of the horizon at equidistant directions around the point of interest, in degrees. Starting at north and moving clockwise. The series '0,10,20,30,40,15,25,5' would mean the horizon height is 0° due north, 10° for north-east, 20° for east, 30° for south-east, etc.
        raddatabase: str, default = None,
          Name of the radiation database (DB): "PVGIS-SARAH" for Europe, Africa and Asia or "PVGIS-NSRDB" for the Americas between 60°N and 20°S, "PVGIS-ERA5" and "PVGIS-COSMO" for Europe (including high-latitudes), and "PVGIS-CMSAF" for Europe and Africa (will be deprecated). The default DBs are PVGIS-SARAH, PVGIS-NSRDB and PVGIS-ERA5 based on the chosen location (see Figure xx).
        startyear: int, default = None,
          First year of the output of monthly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the first year of the DB.
        endyear: int, default = None,
          Final year of the output of monthly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the last year of the DB.
        horirrad: int, default = 1,
          Output horizontal plane irradiation. Value of 1 for "yes". All other values (or no value) mean "no".
        optrad: int, default = 0,
          Output annual optimal angle plane irradiation. Value of 1 for "yes". All other values (or no value) mean "no".
        selectrad: int, default = 0,
          Output irradiation on plane of selected inclination. Value of 1 for "yes". All other values (or no value) mean "no".
        angle: int, default = 0,
        	Inclination
          Example of the minimum usage:
            n angle for the selected inclination irradiation option.
        mr_dni: int, default = 1,
          Output direct normal irradiation. Value of 1 for "yes". All other values (or no value) mean "no".
        d2g: int, default = 1,
          Output monthly values of the ratio of diffuse to global radiation (horizontal plane). Value of 1 for "yes". All other values (or no value) mean "no".
        avtemp: int, default = 1,
          Output monthly average values of daily (24h) temperature. Value of 1 for "yes". All other values (or no value) mean "no".
        outputformat: st, defaultr = "json",
          Type of output. Choices are: "csv" for the normal csv output with text explanations, "basic" to get only the data output with no text, and "json".
        url: str, default = "http://re.jrc.ec.europa.eu/api/v5_2/",
            PVGIS 5.1: https://re.jrc.ec.europa.eu/api/v5_1/
            PVGIS 5.2: https://re.jrc.ec.europa.eu/api/v5_2/

      """
        import requests
        import pandas as pd

        self.latitude = latitude
        self.longitude = longitude
        self.usehorizon = usehorizon
        self.userhorizon = userhorizon
        self.raddatabase = raddatabase
        self.startyear = startyear
        self.endyear = endyear
        self.horirrad = horirrad
        self.selectrad = selectrad
        self.angle = angle
        self.mr_dni = mr_dni
        self.d2g = d2g
        self.avtemp = avtemp
        self.outputformat = outputformat
        self.url = url
        self.data = None

        url = self.url + f"MRcalc?lat={self.latitude}&lon={self.longitude}"

        if self.usehorizon != None:
            url = url + f"&usehorizon={self.usehorizon}"
        if self.userhorizon != None:
            url = url + f"&userhorizon={self.userhorizon}"
        if self.raddatabase != None:
            url = url + f"&raddatabase={self.raddatabase}"
        if self.startyear != None:
            url = url + f"&startyear={self.startyear}"
        if self.endyear != None:
            url = url + f"&endyear={self.endyear}"
        if self.horirrad != None:
            url = url + f"&horirrad={self.horirrad}"
        if self.selectrad != None:
            url = url + f"&selectrad={self.selectrad}"
        if self.angle != None:
            url = url + f"&angle={self.angle}"
        if self.mr_dni != None:
            url = url + f"&mr_dni={self.mr_dni}"
        if self.avtemp != None:
            url = url + f"&avtemp={self.avtemp}"
        if self.d2g != None:
            url = url + f"&d2g={self.d2g}"
        if self.outputformat != None:
            url = url + f"&outputformat={self.outputformat}"

        self.url = url
        data = requests.get(url).json()
        try:
            outputs = data["outputs"]["monthly"]
            outputs = pd.json_normalize(outputs)

            inputs = data["inputs"]

            meta = data["meta"]
        except:
            class FaultyDataInput(Exception):
              pass
            raise FaultyDataInput("Error with the PVGIS input.")

        self.data = inputs, outputs, meta

        return self.data

    def retrieve_daily(self, latitude: float, longitude: float, month: int, URL_ONLY : int = 0, usehorizon: int = 1, userhorizon: int = None, raddatabase: str = None, angle: int = 0, aspect: int = 0, global_irr: int = 1, glob_2axis: int = 0, clearsky: int = 1, clearsky_2axis: int = 0, showtemperatures: int = 1, localtime: int = 1, outputformat: str = "json", url: str = "http://re.jrc.ec.europa.eu/api/v5_2/", ) -> object:
        """
        Daily Data: This method retrieves real-world data using the PVGIS-API.
        The months count start at January=0 and December=11
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metadata

        Parameters
        ----------
        latitude: float,
          Latitude, in decimal degrees, south is negative.
        longitude: float
          Longitude, in decimal degrees, west is negative.
        month: int,
          The value of this parameter should be the number of the month, starting at 1 for January. If you give the value 0 (zero) you will instead get data for all the months.
        usehorizon: int, default = 1,
          Calculate taking into account shadows from high horizon. Value of 1 for "yes".
        userhorizon: int, default = None,
          Height of the horizon at equidistant directions around the point of interest, in degrees. Starting at north and moving clockwise. The series '0,10,20,30,40,15,25,5' would mean the horizon height is 0° due north, 10° for north-east, 20° for east, 30° for south-east, etc.
        raddatabase: str, default = None,
          Name of the radiation database (DB): "PVGIS-SARAH" for Europe, Africa and Asia or "PVGIS-NSRDB" for the Americas between 60°N and 20°S, "PVGIS-ERA5" and "PVGIS-COSMO" for Europe (including high-latitudes), and "PVGIS-CMSAF" for Europe and Africa (will be deprecated). The default DBs are PVGIS-SARAH, PVGIS-NSRDB and PVGIS-ERA5 based on the chosen location (see Figure xx).
        angle: int, default = 0,
          Inclination angle from horizontal plane of the (fixed) PV system.
        aspect: int, default = 0,
          Orientation (azimuth) angle of the (fixed) PV system, 0=south, 90=west, -90=east.
        global_irr: int, default = 1,
          Output the global, direct and diffuse in-plane irradiances. Value of 1 for "yes". All other values (or no value) mean "no".
        glob_2axis: int, default = 0,
          Output the global, direct and diffuse two-axis tracking irradiances. Value of 1 for "yes". All other values (or no value) mean "no".
        clearsky: int, default = 0,
          Output the global clear-sky irradiance. Value of 1 for "yes". All other values (or no value) mean "no".
        clearsky_2axis: in, defaultt = 0,
          Output the global clear-sky two-axis tracking irradiance. Value of 1 for "yes". All other values (or no value) mean "no".
        showtemperatures: int, default = 1,
          Output the daily temperature profile. Value of 1 for "yes". All other values (or no value) mean "no".
        localtime: int, default = 1,
          Output the time in the local time zone (not daylight saving time), instead of UTC. Value of 1 for "yes". All other values (or no value) mean "no".
        outputformat: str, default = "json",
          Type of output. Choices are: "csv" for the normal csv output with text explanations, "basic" to get only the data output with no text, and "json".
        url: str, default = "http://re.jrc.ec.europa.eu/api/v5_2/",
            PVGIS 5.1: https://re.jrc.ec.europa.eu/api/v5_1/
            PVGIS 5.2: https://re.jrc.ec.europa.eu/api/v5_2/

      """
        import requests
        import pandas as pd
        import time

        self.month = month
        self.latitude = latitude
        self.longitude = longitude
        self.usehorizon = usehorizon
        self.userhorizon = userhorizon
        self.raddatabase = raddatabase
        self.angle = angle
        self.aspect = aspect
        self.global_irr = global_irr
        self.glob_2axis = glob_2axis
        self.clearsky = clearsky
        self.clearsky_2axis = clearsky_2axis
        self.showtemperatures = showtemperatures
        self.localtime = localtime
        self.outputformat = outputformat
        self.url = url
        self.data = None

        url = (
            self.url
            + f"DRcalc?lat={self.latitude}&lon={self.longitude}&month={self.month}"
        )

        if self.usehorizon != None:
            url = url + f"&usehorizon={self.usehorizon}"
        if self.userhorizon != None:
            url = url + f"&userhorizon={self.userhorizon}"
        if self.raddatabase != None:
            url = url + f"&raddatabase={self.raddatabase}"
        if self.angle != None:
            url = url + f"&angle={self.angle}"
        if self.aspect != None:
            url = url + f"&aspect={self.aspect}"
        if self.global_irr != None:
            url = url + f"&global={self.global_irr}"
        if self.glob_2axis != None:
            url = url + f"&glob_2axis={self.glob_2axis}"
        if self.clearsky != None:
            url = url + f"&clearsky={self.clearsky}"
        if self.clearsky_2axis != None:
            url = url + f"&clearsky_2axis={self.clearsky_2axis}"
        if self.showtemperatures != None:
            url = url + f"&showtemperatures={self.showtemperatures}"
        if self.localtime != None:
            url = url + f"&localtime={self.localtime}"
        if self.outputformat != None:
            url = url + f"&outputformat={self.outputformat}"
        if URL_ONLY == 1:
          return url, url, url
        self.url = url

        data = requests.get(url)
        status_code = data.status_code
        if status_code == 429:
          return '429','429','429'
        data = data.json()
        
        try:
           
            outputs = data["outputs"]["daily_profile"]
            outputs = pd.json_normalize(outputs)
            outputs = outputs.set_index("time")
            inputs = data["inputs"]
            meta = data["meta"]

        except Exception as e:
            class FaultyDataInput(Exception):
              pass
            raise FaultyDataInput(f"Error with the PVGIS input:\n{e}")


        input_tmy, output_tmy, metadata_tmy = PVGIS().retrieve_tmy(latitude,longitude)
        while input_tmy=='429':
          time.sleep(1)
          input_tmy, output_tmy, metadata_tmy = PVGIS().retrieve_tmy(latitude,longitude)



        output_tmy = output_tmy[output_tmy.index.month == self.month]

        df = pd.DataFrame()
        df = pd.DataFrame(index=outputs.index)
        wind_speed = []

        for hour in range(0,24,1):
          wind_speed.append(output_tmy.iloc[hour:24+hour, :]['WS10m'].mean())

        outputs['WS10m'] = wind_speed

        if(outputs['T2m'].mean() == 0 or outputs['WS10m'].mean() == 0):
          if 'v5_2' in self.url:
            return PVGIS().retrieve_daily(self.latitude, self.longitude, self.month, self.usehorizon, self.userhorizon, self.raddatabase, self.angle, self.aspect, self.global_irr, self.glob_2axis, self.clearsky, self.clearsky_2axis, self.showtemperatures, self.localtime, self.outputformat, url= "http://re.jrc.ec.europa.eu/api/v5_1/", )
        self.data = inputs, outputs, meta
        return self.data

    def retrieve_tmy(self, latitude: float,
                     longitude: float,
                     URL_ONLY: int = 0,
                     usehorizon: int = 1,
                     userhorizon: int = None,
                     startyear: int = None,
                     endyear: int = None,
                     outputformat: str = "json",
                     url: str = "http://re.jrc.ec.europa.eu/api/v5_2/", ) -> object:
        """
        Daily Data: This method retrieves real-world data using the PVGIS-API.
        The months count start at January=0 and December=11
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metadata

        Parameters
        ----------
        latitude: float,
          Latitude, in decimal degrees, south is negative.
        longitude: float
          Longitude, in decimal degrees, west is negative.
        startyear: int, default = None,
          First year of the output of monthly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the first year of the DB.
        endyear: int, default = None,
          Final year of the output of monthly averages. Availability varies with the temporal coverage of the radiation DB chosen. The default value is the last year of the DB.
        usehorizon: int, default = 1,
          Calculate taking into account shadows from high horizon. Value of 1 for "yes".
        userhorizon: int, default = None,
          Height of the horizon at equidistant directions around the point of interest, in degrees. Starting at north and moving clockwise. The series '0,10,20,30,40,15,25,5' would mean the horizon height is 0° due north, 10° for north-east, 20° for east, 30° for south-east, etc.
        outputformat: str, default = "json",
          Type of output. Choices are: "csv" for the normal csv output with text explanations, "basic" to get only the data output with no text, and "json".
        url: str, default = "http://re.jrc.ec.europa.eu/api/v5_2/",
            PVGIS 5.1: https://re.jrc.ec.europa.eu/api/v5_1/
            PVGIS 5.2: https://re.jrc.ec.europa.eu/api/v5_2/

      """
        import requests
        import pandas as pd

        self.latitude = latitude
        self.longitude = longitude
        self.usehorizon = usehorizon
        self.userhorizon = userhorizon
        self.startyear = startyear
        self.endyear = endyear
        self.outputformat = outputformat
        self.url = url
        self.data = None

        url = (
            self.url
            + f"tmy?lat={self.latitude}&lon={self.longitude}"
        )

        if self.usehorizon != None:
            url = url + f"&usehorizon={self.usehorizon}"
        if self.userhorizon != None:
            url = url + f"&userhorizon={self.userhorizon}"
        if self.startyear != None:
            url = url + f"&startyear={self.startyear}"
        if self.endyear != None:
            url = url + f"&endyear={self.endyear}"
        if self.outputformat != None:
            url = url + f"&outputformat={self.outputformat}"

        if URL_ONLY == 1:
          return url,url, url
        self.url = url
        data = requests.get(url)
        status_code = data.status_code
        if status_code == 429:
          return '429','429','429'
        data = data.json()
        try:
            outputs = data["outputs"]["tmy_hourly"]
            outputs = pd.json_normalize(outputs)
            outputs["time(UTC)"] = pd.to_datetime(outputs["time(UTC)"], format="%Y%m%d:%H%M")
            outputs = outputs.set_index("time(UTC)")
            outputs.index.names = ['time']
            inputs = data["inputs"]
            meta = data["meta"]

        except:
            class FaultyDataInput(Exception):
              pass
            raise FaultyDataInput("Error with the PVGIS input.")

        outputs.rename(columns = {'G(h)':'Global irradiance on the horizontal plane',
                                'RH':'relative humidity',
                                'Gb(n)':' Beam/direct irradiance on a plane always normal to sun rays',
                                'T2m':'2m Air Temperature',
                                'Gd(h)': 'Diffuse irradiance on the horizontal plane',
                                }, inplace = True)

        self.data = inputs, outputs, meta
        return self.data
   
   
    def retrieve_all_year(self, location, panel_tilt, azimuth):
      import pandas as pd
      import concurrent.futures
      import time

      if panel_tilt == 'Optimal':
        input , _, _ = PVGIS().retrieve_hourly(
                                            latitude=location.latitude,
                                            longitude=location.longitude,
                                            optimalinclination=1
                                            )
        panel_tilt = input['mounting_system']['fixed']['slope']['value']
        #print("Slope of " + str(panel_tilt))

      def load_data(location,panel_tilt, azimuth, month_):
        inputs, data , metadata = PVGIS().retrieve_daily(
                              location.latitude, 
                              location.longitude, 
                              month= month_,
                              angle=panel_tilt,
                              aspect=azimuth,
                              glob_2axis = 1)
        while inputs == '429':
          time.sleep(1)
          inputs, data , metadata = PVGIS().retrieve_daily(
                              location.latitude, 
                              location.longitude, 
                              month= month_,
                              angle=panel_tilt,
                              aspect=azimuth,
                              glob_2axis = 1)
                              
                              
        return inputs , data , metadata

      MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]
      import pandas as pd
      outputs = pd.DataFrame()
      with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data, location, panel_tilt, azimuth, month): month for month in MONTHS}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  inputs , data , metadata = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                outputs =  pd.concat([data, outputs])

      
      
      data = outputs.sort_values(by=['month', 'time'])

      data.rename(columns = {   'G(i)':'Global irradiance on a fixed plane',
                                'Gb(i)':'Direct irradiance on a fixed plane',
                                'Gb(n)':'Direct normal irradiance',
                                'T2m':'2m Air Temperature',
                                'WS10m':'10m Wind speed',
                                'G(n)': 'Global irradiance on 2-axis tracking plane',
                                'Gd(i)': 'Diffuse irradiance on a fixed plane',
                                'Gd(n)': 'Diffuse irradiance on 2-axis tracking plane'
                                }, inplace = True)

      self.data = inputs , data , metadata 
      return self.data

    def retrieve_all_year_bifacial(self, location, azimuth):
      import pandas as pd
      import concurrent.futures
      import time

      def load_data(location, azimuth, month_):
        azimuth_backsheet = int(azimuth) + 180
        if azimuth_backsheet <= 180:
          pass
        else:
          azimuth_backsheet = azimuth_backsheet - 360

        inputs, data1 , metadata = PVGIS().retrieve_daily(
                          location.latitude, 
                          location.longitude, 
                          month= month_, 
                          angle = 90, 
                          aspect = azimuth,
                          glob_2axis = 1)
        while inputs == '429':
          time.sleep(1)
          inputs, data1 , metadata = PVGIS().retrieve_daily(
                          location.latitude, 
                          location.longitude, 
                          month= month_, 
                          angle = 90, 
                          aspect = azimuth, 
                          glob_2axis = 1)
        
        inputs2, data2 , metadata2 = PVGIS().retrieve_daily(
                          location.latitude, 
                          location.longitude, 
                          month= month_, 
                          angle = 90, 
                          aspect = azimuth_backsheet, 
                          glob_2axis = 1)
        
        while inputs == '429':
          time.sleep(1)
          inputs2, data2 , metadata2 = PVGIS().retrieve_daily(
                          location.latitude, 
                          location.longitude, 
                          month= month_, 
                          angle = 90, 
                          aspect = azimuth_backsheet, 
                          glob_2axis = 1)
        
    
        data2 = data2.drop(['month','T2m','WS10m'], axis=1)
        data = data1.add(data2, fill_value=0)

        return inputs , data , metadata

      MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]
      import pandas as pd
      outputs = pd.DataFrame()
      with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data, location, azimuth, month): month for month in MONTHS}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  inputs , data , metadata = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                outputs =  pd.concat([data, outputs])

      
      data = outputs.sort_values(by=['month', 'time'])

      data.rename(columns = {   'G(i)':'Global irradiance on a fixed plane',
                                'Gb(i)':'Direct irradiance on a fixed plane',
                                'Gb(n)':'Direct normal irradiance',
                                'T2m':'2m Air Temperature',
                                'WS10m':'10m Wind speed',
                                'G(n)': 'Global irradiance on 2-axis tracking plane',
                                'Gd(i)': 'Diffuse irradiance on a fixed plane',
                                'Gd(n)': 'Diffuse irradiance on 2-axis tracking plane'
                                }, inplace = True)

      self.data = inputs , data , metadata 
      return self.data

    async def retrieve_all_year_faster(self, location, panel_tilt, azimuth):
      import pandas as pd
      import concurrent.futures
      import time
      import asyncio
      import aiohttp   #!pip install aiohttp aiodns
      semaphore = asyncio.Semaphore(24)
      if panel_tilt == 'Optimal':
        input , _, _ = PVGIS().retrieve_hourly(
                                            latitude=location.latitude,
                                            longitude=location.longitude,
                                            optimalinclination=1
                                            )
        panel_tilt = input['mounting_system']['fixed']['slope']['value']

      def load_data(location,panel_tilt, azimuth, month_):
        inputs, data , metadata = PVGIS().retrieve_daily(
                              location.latitude, 
                              location.longitude, 
                              month= month_,
                              angle=panel_tilt,
                              aspect=azimuth,
                              glob_2axis = 1,
                              URL_ONLY = 1)
                                            
        return data

      async def get(session: aiohttp.ClientSession,url: str) -> dict:
          #print(f"Requesting {url}")
          async with semaphore:
            resp = await session.request('GET', url=url)
            while resp.status == 429:
              resp = await session.request('GET', url=url)
            data = await resp.json()
            if '/tmy?' in url:
              return 'TMY', data
            return 'NORMAL', data

      MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]
      list_of_urls = []
      with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data, location, panel_tilt, azimuth, month): month for month in MONTHS}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  url = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                list_of_urls.append(url)

      _, tmy_url, _ = PVGIS().retrieve_tmy(location.latitude,location.longitude, URL_ONLY = 1)
      list_of_urls.append(tmy_url)

      final_outputs = pd.DataFrame()
      async with aiohttp.ClientSession() as session:
        tasks = []
        for c in list_of_urls:
            tasks.append(get(session=session, url=c))

        total_data = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i in range(len(total_data)):
          type_, data = total_data[i]
          if type_ == 'TMY':
            TMY_DATA = data
            total_data.pop(i)   

      for data in total_data:
        outputs = data[1]["outputs"]["daily_profile"]
        outputs = pd.json_normalize(outputs)
        outputs = outputs.set_index("time")
        final_outputs =  pd.concat([outputs, final_outputs])
        inputs = data[1]["inputs"]
        meta = data[1]["meta"]
      
      output_yearly_tmy = TMY_DATA["outputs"]["tmy_hourly"]
      output_yearly_tmy = pd.json_normalize(output_yearly_tmy)
      output_yearly_tmy["time(UTC)"] = pd.to_datetime(output_yearly_tmy["time(UTC)"], format="%Y%m%d:%H%M")
      output_yearly_tmy = output_yearly_tmy.set_index("time(UTC)")
      output_yearly_tmy.index.names = ['time']

      wind_list_of_lists = []
      for month in range(1,13):
        output_tmy = output_yearly_tmy[output_yearly_tmy.index.month == month]

        wind_speed = []

        for hour in range(0,24,1):
          wind_speed.append(output_tmy.iloc[hour:24+hour, :]['WS10m'].mean())
        wind_list_of_lists.append(wind_speed)
      flat_list = [item for sublist in wind_list_of_lists for item in sublist]
      final_outputs = final_outputs.sort_values(by=['month', 'time'])
      final_outputs['WS10m'] = flat_list
      
      final_outputs.rename(columns = {   'G(i)':'Global irradiance on a fixed plane',
                                      'Gb(i)':'Direct irradiance on a fixed plane',
                                      'Gb(n)':'Direct normal irradiance',
                                      'T2m':'2m Air Temperature',
                                      'WS10m':'10m Wind speed',
                                      'G(n)': 'Global irradiance on 2-axis tracking plane',
                                      'Gd(i)': 'Diffuse irradiance on a fixed plane',
                                      'Gd(n)': 'Diffuse irradiance on 2-axis tracking plane'
                                      }, inplace = True)


      return inputs, final_outputs, meta

    async def retrieve_all_year_bifacial_faster(self, location, azimuth):
      import pandas as pd
      import concurrent.futures
      import time
      import asyncio
      import aiohttp   #!pip install aiohttp aiodns
      semaphore = asyncio.Semaphore(24)

      def load_data(location, azimuth, month_):
            azimuth_backsheet = int(azimuth) + 180
            if azimuth_backsheet <= 180:
              pass
            else:
              azimuth_backsheet = azimuth_backsheet - 360
            inputs, data1 , metadata = PVGIS().retrieve_daily(
                              location.latitude, 
                              location.longitude, 
                              month= month_, 
                              angle = 90, 
                              aspect = azimuth,
                              URL_ONLY = 1,
                              glob_2axis = 1)
            
            inputs2, data2 , metadata2 = PVGIS().retrieve_daily(
                              location.latitude, 
                              location.longitude, 
                              month= month_, 
                              angle = 90, 
                              URL_ONLY = 1,
                              aspect = azimuth_backsheet, 
                              glob_2axis = 1)  
                                    
            return data1 , data2

      async def get(session: aiohttp.ClientSession,url: str) -> dict:
          #print(f"Requesting {url}")
          async with semaphore:
            resp = await session.request('GET', url=url)
            while resp.status == 429:
              resp = await session.request('GET', url=url)
            data = await resp.json()
            if '/tmy?' in url:
              return 'TMY', data
            return 'NORMAL', data

      MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]
      list_of_urls = []
      with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
          # Start the load operations and mark each future with its URL
          future_to_url = {executor.submit(load_data, location, azimuth, month): month for month in MONTHS}
          for future in concurrent.futures.as_completed(future_to_url):
              url = future_to_url[future]
              try:
                  url1, url2 = future.result()
              except Exception as exc:
                  class FaultyDataInput(Exception):
                    pass
                  raise FaultyDataInput(exc)
              else:
                list_of_urls.append(url1)
                list_of_urls.append(url2)

      _, tmy_url, _ = PVGIS().retrieve_tmy(location.latitude,location.longitude, URL_ONLY = 1)
      list_of_urls.append(tmy_url)

      final_outputs = pd.DataFrame()
      async with aiohttp.ClientSession() as session:
        tasks = []
        for c in list_of_urls:
            tasks.append(get(session=session, url=c))

        total_data = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i in range(len(total_data)):
          type_, data = total_data[i]
          if type_ == 'TMY':
            TMY_DATA = data
            total_data.pop(i)   
      azimuth = total_data[0][1]['inputs']['plane']['fixed']['azimuth']['value']  

      data1 = pd.DataFrame()
      data2 = pd.DataFrame()

      for data in total_data:

        if azimuth == data[1]['inputs']['plane']['fixed']['azimuth']['value']:
          outputs = data[1]["outputs"]["daily_profile"]
          outputs = pd.json_normalize(outputs)
          outputs = outputs.set_index("time")
          data1 =  pd.concat([outputs, data1])
          inputs = data[1]["inputs"]
          meta = data[1]["meta"]
        else:
          outputs = data[1]["outputs"]["daily_profile"]
          outputs = pd.json_normalize(outputs)
          outputs = outputs.set_index("time")
          data2 = pd.concat([outputs, data2])
      
      data2 = data2.sort_values(by=['month', 'time'])
      data1 = data1.sort_values(by=['month', 'time'])
      data2 = data2.drop(['month','T2m'], axis=1)
      final_outputs = data1.add(data2, fill_value=0)

        
      output_yearly_tmy = TMY_DATA["outputs"]["tmy_hourly"]
      output_yearly_tmy = pd.json_normalize(output_yearly_tmy)
      output_yearly_tmy["time(UTC)"] = pd.to_datetime(output_yearly_tmy["time(UTC)"], format="%Y%m%d:%H%M")
      output_yearly_tmy = output_yearly_tmy.set_index("time(UTC)")
      output_yearly_tmy.index.names = ['time']

      wind_list_of_lists = []
      for month in range(1,13):
        output_tmy = output_yearly_tmy[output_yearly_tmy.index.month == month]

        wind_speed = []

        for hour in range(0,24,1):
          wind_speed.append(output_tmy.iloc[hour:24+hour, :]['WS10m'].mean())
        wind_list_of_lists.append(wind_speed)
        
      flat_list = [item for sublist in wind_list_of_lists for item in sublist]
      final_outputs = final_outputs.sort_values(by=['month', 'time'])
      final_outputs['WS10m'] = flat_list
      
      final_outputs.rename(columns = {   'G(i)':'Global irradiance on a fixed plane',
                                      'Gb(i)':'Direct irradiance on a fixed plane',
                                      'Gb(n)':'Direct normal irradiance',
                                      'T2m':'2m Air Temperature',
                                      'WS10m':'10m Wind speed',
                                      'G(n)': 'Global irradiance on 2-axis tracking plane',
                                      'Gd(i)': 'Diffuse irradiance on a fixed plane',
                                      'Gd(n)': 'Diffuse irradiance on 2-axis tracking plane'
                                      }, inplace = True)

      
      return inputs, final_outputs, meta

