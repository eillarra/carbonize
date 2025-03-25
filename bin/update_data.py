"""Update data files for the carbonize package."""

import csv
import os
import pickle

from carbonize.data.parsers import IATAParser, ICAOParser


DATA_DIR = "carbonize/data"


def dump_data(data, filename: str, format="pickle") -> None:
    """Dump data to a file."""
    if format == "pickle":
        with open(os.path.join(DATA_DIR, f"{filename}.pkl"), "wb") as file:
            pickle.dump(data, file)
    if format == "csv":
        with open(os.path.join(DATA_DIR, f"{filename}.csv"), "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)


"""Process the ICAO Carbon Emissions Calculator Methodology document."""

icao = ICAOParser()
dump_data(icao.get_aircrafts(), "icao_aircrafts")
dump_data(icao.get_routes(), "icao_load_factors")


"""Get IATA airport information from https://ourairports.com/data/"""

iata = IATAParser()
dump_data(iata.get_airports(), "iata_airports")
