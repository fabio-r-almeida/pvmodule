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

    def retrieve_hourly(
        self,
        latitude: float,
        longitude: float,
        month: str = None,
        usehorizon: int = 1,
        userhorizon: int = None,
        raddatabase: str = None,
        startyear: int = None,
        endyear: int = None,
        pvcalculation: int = 0,
        peakpower: float = None,
        pvtechchoice: str = "crystSi",
        mountingplace: str = "free",
        loss: float = None,
        trackingtype: int = 0,
        surface_tilt: float = 0,
        surface_azimuth: float = 0,
        optimalinclination: int = 0,
        optimalangles: int = 0,
        components: int = 0,
        outputformat: str = "json",
        url: str = "http://re.jrc.ec.europa.eu/api/v5_2/",
    ) -> object:
        """
        Hourly Data: This method retrieves real-world data using the PVGIS-API.
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metedata

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
            url = url + f"&surface_tilt={self.surface_tilt}"
        if self.surface_azimuth != None:
            url = url + f"&surface_azimuth={self.surface_azimuth}"
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
            return print(f"Error: {data}")

        self.data = inputs, outputs, meta
        return self.data

    def retrieve_monthly(
        self,
        latitude: float,
        longitude: float,
        usehorizon: int = 1,
        userhorizon: int = None,
        raddatabase: str = None,
        startyear: int = None,
        endyear: int = None,
        horirrad: int = 1,
        optrad: int = 0,
        selectrad: int = 0,
        angle: int = 0,
        mr_dni: int = 1,
        d2g: int = 1,
        avtemp: int = 1,
        outputformat: str = "json",
        url: str = "http://re.jrc.ec.europa.eu/api/v5_2/",
    ) -> object:
        """
        Monthly Data: This method retrieves real-world data using the PVGIS-API.
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metedata

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
            return print(f"Error: {data}")

        self.data = inputs, outputs, meta
        return self.data

    def retrieve_daily(
        self,
        latitude: float,
        longitude: float,
        month: int,
        usehorizon: int = 1,
        userhorizon: int = None,
        raddatabase: str = None,
        angle: int = 0,
        aspect: int = 0,
        global_irr: int = 1,
        glob_2axis: int = 0,
        clearsky: int = 0,
        clearsky_2axis: int = 0,
        showtemperatures: int = 1,
        localtime: int = 1,
        outputformat: str = "json",
        url: str = "http://re.jrc.ec.europa.eu/api/v5_2/",
    ) -> object:
        """
        Daily Data: This method retrieves real-world data using the PVGIS-API.
        The months count start at January=0 and December=11
        ...
        It outputs 3 dataframes with the following structure:
        Inputs , Outputs, Metedata

        """
        import requests
        import pandas as pd

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

        self.url = url
        data = requests.get(url).json()
        try:
            outputs = data["outputs"]["daily_profile"]
            outputs = pd.json_normalize(outputs)
            outputs = outputs.set_index("time")

            inputs = data["inputs"]

            meta = data["meta"]

        except:
            return print(f"Error: {data}")

        self.data = inputs, outputs, meta
        return self.data
