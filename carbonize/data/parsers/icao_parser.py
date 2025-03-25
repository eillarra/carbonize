"""ICAO Carbon Emissions Calculator Methodology data parser."""

import io
import re
from operator import itemgetter

import pypdf
import requests

from carbonize.type_definitions import Aircraft, Route


class ICAOParser:
    """Parse ICAO Carbon Emissions Calculator Methodology data from a URL or filename."""

    default_url = (
        "https://applications.icao.int/icec/Methodology%20ICAO%20Carbon%20Emissions%20Calculator_v13_Final.pdf"
    )
    url = None
    filename = None
    reader: pypdf.PdfReader

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
                self.reader = pypdf.PdfReader(io.BytesIO(res.content))
        elif self.filename:
            with open(self.filename, "rb") as f:
                self.reader = pypdf.PdfReader(io.BytesIO(f.read()))

    def _extract_text(self, page: pypdf.PageObject) -> str:
        """Extract text as in `pypdf.pdf.extractText` method, but treating spaces differently."""
        contents = pypdf.generic.ContentStream(page.get_contents(), page.pdf)
        text = ""

        for operands, operator in contents.operations:
            if operator == b"TJ":
                text += "".join([i for i in operands[0] if isinstance(i, str)])

        return text

    def _split_list_and_fill(self, lst: list, n: int):
        """Yield successive n-sized chunks from lst. If the last chunk is smaller than n, fill it with None."""
        for i in range(0, len(lst), n):
            chunk = lst[i : i + n]
            if len(chunk) < n:
                chunk.extend([None] * (n - len(chunk)))
            yield chunk

    def get_aircraft_code_pairs(self) -> list[tuple[str, str]]:
        """Return a dictionary of aircraft codes and their equivalents."""
        tmp_list: list[tuple[str, str]] = []
        pages = range(13, 16)

        for page in pages:
            text = self._extract_text(self.reader.pages[page - 1])
            page_data = [word.strip() for word in text.split(" ") if len(word.strip()) == 3]
            tmp_list.extend(self._split_list_and_fill(page_data, 2))

        return sorted(tmp_list, key=itemgetter(0))

    def get_aircrafts(self) -> list[Aircraft]:
        """Return a list of Aircraft objects."""
        data_columns = 20
        total_columns = data_columns + 1
        fuel_consumption: list[tuple[str, ...]] = []

        for page in range(16, 23):
            text = self._extract_text(self.reader.pages[page - 1])
            chunks = [line.strip() for line in text.split("  ") if line.strip()]
            chunks[0] = chunks[0][chunks[0].index("Code") :]
            split_chunks = [chunk.split() for chunk in chunks]
            final_chunks = [
                sub_chunk for chunk in split_chunks for sub_chunk in self._split_list_and_fill(chunk, total_columns)
            ]
            cleaned_data = [tuple(chunk) for chunk in final_chunks[1:]]
            fuel_consumption.extend(cleaned_data)

        aircraft_codes = self.get_aircraft_code_pairs()
        consumptions = {d[0]: d[1:] for d in sorted(fuel_consumption, key=itemgetter(0))}
        aircrafts: list[Aircraft] = []

        for code in aircraft_codes:
            try:
                aircrafts.append(Aircraft(code[0], [(int(v) if v else None) for v in consumptions[code[1]]]))
            except KeyError:
                # some aircrafts don't have fuel consumption data so we ignore them
                continue

        return aircrafts

    def get_routes(self) -> list[Route]:
        """Return a list of Route objects with load factors."""
        load_factors: list[str] = []

        for page in range(11, 13):
            text = self._extract_text(self.reader.pages[page - 1]).strip()
            page_data = re.split(r"[ ](\d+)[ ]", text)
            if page_data[0] == str(page):
                page_data.pop(0)
            load_factors.extend(page_data)

        routes = []

        for f in self._split_list_and_fill(load_factors[load_factors.index("1") :], 2):
            tmp = re.split(r"[ ](\d*[.]\d*)", f[1])
            routes.append(Route(f[0], tmp[0], tmp[1], tmp[3]))

        return routes
