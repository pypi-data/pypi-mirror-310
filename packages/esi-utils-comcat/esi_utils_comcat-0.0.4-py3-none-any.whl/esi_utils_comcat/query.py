# stdlib imports
import json
import time
import warnings
from datetime import datetime
from urllib import request
from urllib.error import HTTPError

import requests

URL_TEMPLATE = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson"
)
REGIONS_URL = "http://earthquake.usgs.gov/ws/geoserve/regions.json?latitude=[LAT]&longitude=[LON]"  # noqa
PLACES_URL = "http://earthquake.usgs.gov/ws/geoserve/places.json?latitude=[LAT]&longitude=[LON]&maxradiuskm=[RADIUS]&minpopulation=[POP]&type=geonames"  # noqa

TIMEOUT = 15
WAITSECS = 3


def _get_data(url, timeout):
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        http_error = HTTPError(url, code=response.status_code)
        raise http_error

    data = response.text
    return data


def _get_url_data(url, timeout=TIMEOUT):
    try:
        data = _get_data(url, timeout)
    except HTTPError as htpe:
        if htpe.code == 503:
            try:
                time.sleep(WAITSECS)
                data = _get_data(url, timeout)
            except Exception as msg:
                raise Exception(f'Error downloading data from url {url}.  "{msg}".')
    return data


class GeoServe(object):
    """Class to wrap around the NEIC GeoServe web service."""

    def __init__(self, lat, lon, maxradius=500, minpop=1000):
        """
        Initialize object with data from web service for a given
        latitude/longitude coordinate.

        Args:
            lat (float): Desired latitude.
            lon (float): Desired longitude.
            maxradius (float):  Search radius (in kilometers) from the center point.
            minpop (int): Limit results to places where population is greater than or
                equal to minpop.

        Raises:
            Exception if the GeoServe URL cannot be reached after two attempts,
            and a suitable timeout period.
        """
        regurl = REGIONS_URL.replace("[LAT]", str(lat))
        regurl = regurl.replace("[LON]", str(lon))
        placeurl = PLACES_URL.replace("[LAT]", str(lat))
        placeurl = placeurl.replace("[LON]", str(lon))
        placeurl = placeurl.replace("[RADIUS]", str(maxradius))
        placeurl = placeurl.replace("[POP]", str(minpop))
        self._placedict = self._getJSONContent(placeurl)
        self._regdict = self._getJSONContent(regurl)

    def getPlaces(self):
        """Get a list of geojson-like features describing nearest populated places.

        Returns:
            list: List of dictionaries, with fields:
                  - type: "Feature"
                  - id: Database ID
                  - geometry: Dictionary with fields:
                    - coordinates: List of longitude, latitude, elevation.
                  - properties: Dictionary with fields:
                    - admin1_code: "State" level code (i.e., "CO" in the US)
                    - admin1_name: "State" level name, (i.e., "Colorado" in the US)
                    - azimuth: Direction from input latitude/longitude to this location.
                    - country_code: Two letter country code of location ("US").
                    - country_name: Full country name ("United States").
                    - distance: Distance in km from input lat/lon to this location.
                    - feature_class: See http://www.geonames.org/export/codes.html.
                    - feature_code: See http://www.geonames.org/export/codes.html.
                    - name: Unicode name of location (i.e., "Golden").
                    - population: Population of location.
        """
        return self._placedict["geonames"]["features"]

    def getRegions(self):
        """Get a dictionary of region information about input latitude/longitude.

        Returns:
            dict: geojson-like dictionaries, described here:
                https://earthquake.usgs.gov/ws/geoserve/regions.php
                The 'metadata' dictionary is omitted.
        """
        self._regdict.get("metadata", None)
        return self._regdict

    def getAuthoritative(self):
        """Return the authoritative region network code and type.

        Example:
        ('NA', 'anss', or 'contributor').

        Returns:
            Tuple of (authoritative region, region type)
        """
        auth_source = "US"
        auth_type = "NA"
        if len(self._regdict["authoritative"]["features"]):
            auth_source = self._regdict["authoritative"]["features"][0]["properties"][
                "network"
            ]
            # We seem to have all the worlds networks in geoserve, not just
            # ANSS.  A type of 'anss' indicates that this region is an ANSS
            # one.
            auth_type = self._regdict["authoritative"]["features"][0]["properties"][
                "type"
            ]
        return (auth_source, auth_type)

    def _getJSONContent(self, url):
        data = _get_url_data(url, timeout=TIMEOUT)
        content = json.loads(data)
        return content


class ComCatInfo(object):
    def __init__(self, eventid):
        url = URL_TEMPLATE.replace("[EVENTID]", eventid)
        try:
            data = _get_url_data(url)
            self._jdict = json.loads(data)
        except Exception as e:
            msg = "Could not connect to ComCat server."
            raise Exception(msg).with_traceback(e.__traceback__)

    def getAssociatedIds(self):
        """Query ComCat for the event IDs associated with input ID.

        Returns:
            Tuple of (authoritative event ID, all other IDs associated
            with event).
        """
        allids = self._jdict["properties"]["ids"].strip(",").split(",")
        authid = self._jdict["id"]
        allids.remove(authid)
        return (authid, allids)

    def getAssociatedSources(self):
        """Query ComCat for the event sources associated with input ID.

        The output list of other sources is guaranteed to correspond to the
        list of other ids, and the authoritative source is guaranteed to
        correspond with the authoritative ID.

        Returns:
            Tuple of (authoritative event source, all other sources associated
            with event)
        """
        # worst case scenario:
        #  authid = 'at1234'
        #  allids = ['atlas4567','ci2008']
        #  allsources = ['atlas','ci','at']

        allsources = self._jdict["properties"]["sources"].strip(",").split(",")
        authid, allids = self.getAssociatedIds()
        newsources = []
        for eid in [authid] + allids:
            slengths = []
            for source in allsources:
                if eid.startswith(source):
                    slengths.append(len(source))
                else:
                    slengths.append(0)
            newsources.append(allsources[slengths.index(max(slengths))])

        authsource = newsources[0]
        newsources.remove(authsource)
        return (authsource, newsources)

    def getEventParams(self):
        """Query ComCat for the event parameters.

        For examples time, lat, lon, depth, and magnitude associated with
        input ID.

        Returns:
            Dictionary containing:
            - time Datetime object representing earthquake origin time in UTC.
            - lat Origin latitude.
            - lon Origin longitude.
            - depth Origin depth.
            - magnitude Origin magnitude.
        """
        lon, lat, depth = self._jdict["geometry"]["coordinates"]
        itime = self._jdict["properties"]["time"]
        etime = datetime.utcfromtimestamp(int(itime / 1000))
        mag = self._jdict["properties"]["mag"]
        edict = {
            "time": etime,
            "lat": lat,
            "lon": lon,
            "depth": depth,
            "magnitude": mag,
        }
        return edict

    def getLocation(self):
        """Query ComCat for the location string associated with input ID.

        Returns:
            Location string (i.e. "24km NE of Dharchula, India")
        """
        location = self._jdict["properties"]["place"]
        return location

    def getTsunami(self):
        """Query ComCat for the location string associated with input ID.

        Returns:
            int: 1 if a tsunami message was received from NOAA, 0 otherwise.
        """
        tsunami = self._jdict["properties"]["tsunami"]
        return tsunami

    def getShakeGrid(self, local_file=None):
        """Download ShakeMap grid.xml file for given event.

        Args:
            local_file: Path to local file where grid.xml file should be
                downloaded.

        Returns:
            url of ShakeMap grid.xml file, path to local file containing
            grid.xml file data if local_file specified, or None if connection
            to ComCat fails.
        """
        try:
            shake_url = self._jdict["properties"]["products"]["shakemap"][0][
                "contents"
            ]["download/grid.xml"]["url"]
            if local_file is not None:
                data = _get_url_data(shake_url)
                f = open(local_file, "w")
                f.write(data)
                f.close()
                return local_file
            return shake_url
        except BaseException:
            return None

    def getURL(self):
        """Query ComCat for the URL associated with input ID.

        Returns:
            Event URL, i.e https://earthquake.usgs.gov/earthquakes/eventpage/us20007z80
        """
        url = self._jdict["properties"]["url"]
        return url


if __name__ == "__main__":
    positions = [
        {
            "name": "california",
            "coords": (37.28935, -119.53125),
            "source": "NC",
            "type": "anss",
            "place": "Oakhurst",
            "region": "Central California",
        },
        {
            "name": "alaska",
            "coords": (63.379217, -151.699219),
            "source": "AK",
            "type": "anss",
            "place": "Healy",
            "region": "Central Alaska",
        },
        {
            "name": "aleutians",
            "coords": (53.209322, -167.34375),
            "source": "US",
            "type": "NA",
            "place": "Unalaska",
            "region": "Fox Islands, Aleutian Islands, Alaska",
        },
        {
            "name": "japan",
            "coords": (36.700907, 138.999023),
            "source": "US",
            "type": "NA",
            "place": "Numata",
            "region": "eastern Honshu, Japan",
        },
    ]

    for pdict in positions:
        lat, lon = pdict["coords"]
        psource = pdict["source"]
        ptype = pdict["type"]
        pname = pdict["name"]
        place = pdict["place"]
        region = pdict["region"]
        print(f"Testing {pname} authoritative region...")
        gs = GeoServe(lat, lon)
        authsrc, authtype = gs.getAuthoritative()
        assert authsrc == psource
        assert authtype == ptype
        places = gs.getPlaces()
        regdict = gs.getRegions()
        assert places[0]["properties"]["name"] == place
        assert regdict["fe"]["features"][0]["properties"]["name"] == region
