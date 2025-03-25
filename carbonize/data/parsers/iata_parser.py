"""IATA airport information parser."""

import collections
import csv
from operator import attrgetter

import requests

from carbonize.type_definitions import Airport


OurAirport = collections.namedtuple(
    "OurAirport",
    "id ident type name latitude_deg longitude_deg elevation_ft continent iso_country iso_region municipality "
    "scheduled_service icao_code iata_code gps_code local_code home_link wikipedia_link keywords",
)


class IATAParser:
    """Parse IATA airport information from a URL or filename."""

    default_url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    url = None
    filename = None
    source_data = []

    def __init__(self, *, url: str | None = None, filename: str | None = None):
        """Set the URL or filename to parse the data from. URL takes precedence over filename.

        :param url: URL to download the data from.
        :param filename: Filename to read the data from.
        """
        self.url = url
        self.filename = filename

        if not self.url and not self.filename:
            self.url = self.default_url

        self._get_data()

    def _get_data(self):
        if self.url:
            with requests.Session() as s:
                res = s.get(self.url)
                self.source_data = list(csv.reader(res.content.decode("utf-8").splitlines(), delimiter=","))

        elif self.filename:
            with open(self.filename) as f:
                self.source_data = list(csv.reader(f, delimiter=","))

    def get_airports(self) -> list[Airport]:
        """Parse the data from the URL or filename and return the data as a list of Airport objects."""
        airports = [
            OurAirport(*airport) for airport in self.source_data if airport[2] in ["medium_airport", "large_airport"]
        ]
        airports.sort(key=attrgetter("iso_country", "municipality"))
        data = []

        for a in airports:
            data.append(
                Airport(a.iata_code, a.iso_country, a.municipality, float(a.latitude_deg), float(a.longitude_deg))
            )

        return data
