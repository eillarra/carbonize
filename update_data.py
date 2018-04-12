import collections
import csv
import io
import PyPDF2
import re
import requests

from operator import attrgetter, itemgetter
from PyPDF2.pdf import ContentStream
from typing import List, Tuple


DATA_FOLDER = 'carbonize/data'


with requests.Session() as s:
    res = s.get('https://www.icao.int/environmental-protection/CarbonOffset/Documents/'
                'Methodology%20ICAO%20Carbon%20Calculator_v10-2017.pdf')
    reader = PyPDF2.PdfFileReader(io.BytesIO(res.content))


def chunk_list(initial_list: List, elements: int):
    return list(zip(*[initial_list[i::elements] for i in range(elements)]))


def extract_text(page: PyPDF2.pdf.PageObject) -> str:
    """
    This is inspired by the `PyPDF2.pdf.extractText` method, but treats spaces differently.
    """
    contents = ContentStream(page.getContents(), page.pdf)
    text = ''

    for operands, operator in contents.operations:
        if operator == b'TJ':
            text += ''.join([i for i in operands[0] if isinstance(i, str)])

    return text


def process_pairs(reader: PyPDF2.PdfFileReader, pages: range):
    tmp_list: List[Tuple[str, str]] = []

    for page in pages:
        text = extract_text(reader.getPage(page - 1))
        page_data = [l.strip() for l in text.split(' ') if len(l.strip()) == 3]
        tmp_list.extend(chunk_list(page_data, 2))

    return sorted(tmp_list, key=itemgetter(0))


# Get aircraft and airport codes

with open('{0}/{1}'.format(DATA_FOLDER, 'icao_aircraft_codes.csv'), 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Aircraft', 'Equivalent'])
    for pair in process_pairs(reader, range(14, 17)):
        writer.writerow(pair)

with open('{0}/{1}'.format(DATA_FOLDER, 'icao_airport_city_codes.csv'), 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Airport', 'City'])
    for pair in process_pairs(reader, range(24, 39)):
        writer.writerow(pair)


# Get fuel consumption

data_columns = 20
fuel_consumption: List[Tuple[str, ...]] = []

for page in range(17, 24):
    text = extract_text(reader.getPage(page - 1))
    page_data = [l.strip() for l in text.replace('  ', ' -').split(' ') if l.strip()]
    chunks = chunk_list(page_data[page_data.index('Code'):], data_columns + 1)
    fuel_consumption.extend(chunks[1:])

with open('{0}/icao_fuel_consumption.csv'.format(DATA_FOLDER), 'w') as file:
    writer = csv.writer(file)
    writer.writerow(chunks[0])
    for data in sorted(fuel_consumption, key=itemgetter(0)):
        writer.writerow([(None if v == '-' else v) for v in data])


# Get load factors

load_factors: List[str] = []

for page in range(12, 14):
    text = extract_text(reader.getPage(page - 1)).strip()
    page_data = re.split(r'[ ](\d+)[ ]', text)
    if page_data[0] == str(page):
        page_data.pop(0)
    load_factors.extend(page_data)

with open('{0}/icao_load_factors.csv'.format(DATA_FOLDER), 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['#', 'Route group', 'Passenger load factor', 'Passenger to freight factor'])
    for data in chunk_list(load_factors[load_factors.index('1'):], 2):
        tmp = re.split(r'[ ](\d*[.]\d*)', data[1])
        writer.writerow([data[0], tmp[0], tmp[1], tmp[3]])


# Get IATA airport information from http://ourairports.com/data/

OurAirport = collections.namedtuple(
    'OurAirport',
    'id ident type name latitude_deg longitude_deg elevation_ft continent iso_country iso_region municipality '
    'scheduled_service gps_code iata_code local_code home_link wikipedia_link keywords'
)

with requests.Session() as s:
    res = s.get('http://ourairports.com/data/airports.csv')
    cr = csv.reader(res.content.decode('utf-8').splitlines(), delimiter=',')
    airports = [OurAirport(*airport) for airport in list(cr) if airport[2] in ['medium_airport', 'large_airport']]
    airports.sort(key=attrgetter('iso_country', 'municipality'))

    with open('{0}/iata_airports.csv'.format(DATA_FOLDER), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['IATA code', 'Country', 'City', 'Latitude', 'Longitude'])
        for a in airports:
            if not a.iata_code or a.latitude_deg == 0 or a.longitude_deg == 0:
                continue
            writer.writerow([
                a.iata_code,
                a.iso_country,
                a.municipality,
                a.latitude_deg,
                a.longitude_deg,
            ])
