import collections
import csv
import io
import os
import pickle
import PyPDF2  # type: ignore
import re
import requests

from operator import attrgetter, itemgetter
from typing import List, Tuple

from carbonize.types import Aircraft, Airport, Route


DATA_DIR = "carbonize/data"


def chunk_list(initial_list: List, elements: int):
    return list(zip(*[initial_list[i::elements] for i in range(elements)]))


def extract_text(page: PyPDF2.pdf.PageObject) -> str:
    """
    This is inspired by the `PyPDF2.pdf.extractText` method, but treats spaces differently.
    """
    contents = PyPDF2.pdf.ContentStream(page.getContents(), page.pdf)
    text = ""

    for operands, operator in contents.operations:
        if operator == b"TJ":
            text += "".join([i for i in operands[0] if isinstance(i, str)])

    return text


def process_pairs(reader: PyPDF2.PdfFileReader, pages: range):
    tmp_list: List[Tuple[str, str]] = []

    for page in pages:
        text = extract_text(reader.getPage(page - 1))
        page_data = [l.strip() for l in text.split(" ") if len(l.strip()) == 3]
        tmp_list.extend(chunk_list(page_data, 2))

    return sorted(tmp_list, key=itemgetter(0))


"""Process the ICAO Carbon Steps Calculator document."""

with requests.Session() as s:
    res = s.get(
        "https://www.icao.int/environmental-protection/CarbonOffset/Documents/"
        "Methodology%20ICAO%20Carbon%20Calculator_v11-2018.pdf"
    )
    reader = PyPDF2.PdfFileReader(io.BytesIO(res.content))

# Get fuel consumption and update aircraft list

data_columns = 20
fuel_consumption: List[Tuple[str, ...]] = []

for page in range(17, 24):
    text = extract_text(reader.getPage(page - 1))
    page_data = [l.strip() for l in text.replace("  ", " -").split(" ") if l.strip()]
    chunks = chunk_list(page_data[page_data.index("Code") :], data_columns + 1)
    fuel_consumption.extend(chunks[1:])

aircraft_codes = process_pairs(reader, range(14, 17))
consumptions = {d[0]: d[1:] for d in sorted(fuel_consumption, key=itemgetter(0))}
aircrafts: List[Aircraft] = []

for code in aircraft_codes:
    try:
        aircrafts.append(
            Aircraft(
                code[0],
                [(None if v == "-" else int(v)) for v in consumptions[code[1]]],
            )
        )
    except KeyError:
        continue

with open(os.path.join(DATA_DIR, "icao_aircrafts.pkl"), "wb") as file:
    pickle.dump(aircrafts, file)

# Update route load factors

load_factors: List[str] = []

for page in range(12, 14):
    text = extract_text(reader.getPage(page - 1)).strip()
    page_data = re.split(r"[ ](\d+)[ ]", text)
    if page_data[0] == str(page):
        page_data.pop(0)
    load_factors.extend(page_data)

routes = []

for f in chunk_list(load_factors[load_factors.index("1") :], 2):
    tmp = re.split(r"[ ](\d*[.]\d*)", f[1])
    routes.append(Route(f[0], tmp[0], tmp[1], tmp[3]))

with open(os.path.join(DATA_DIR, "icao_load_factors.pkl"), "wb") as file:
    pickle.dump(routes, file)


"""Get IATA airport information from http://ourairports.com/data/"""

OurAirport = collections.namedtuple(
    "OurAirport",
    "id ident type name latitude_deg longitude_deg elevation_ft continent iso_country iso_region municipality "
    "scheduled_service gps_code iata_code local_code home_link wikipedia_link keywords",
)

with requests.Session() as s:
    res = s.get("http://ourairports.com/data/airports.csv")
    cr = csv.reader(res.content.decode("utf-8").splitlines(), delimiter=",")
    airports = [OurAirport(*airport) for airport in list(cr) if airport[2] in ["medium_airport", "large_airport"]]
    airports.sort(key=attrgetter("iso_country", "municipality"))
    data = []

    for a in airports:
        data.append(Airport(a.iata_code, a.iso_country, a.municipality, float(a.latitude_deg), float(a.longitude_deg)))

    with open(os.path.join(DATA_DIR, "iata_airports.pkl"), "wb") as file:
        pickle.dump(data, file)
