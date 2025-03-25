===========================
Flight emissions calculator
===========================

The Flight calculator estimates carbon emissions from air travel between airports.

Usage
-----

.. code-block:: python

    from carbonize.calculators.flights import Flight

    step = Flight(
        a="LHR",         # London Heathrow
        b="JFK",         # New York JFK
        aircraft="320",  # Airbus A320
    )

    print(f"Carbon footprint per passenger: {step.co2e_pax} kg CO2e")

Methodology
-----------

The calculation estimates carbon emissions based on:

1. The distance between airports calculated using the great circle method based on coordinates, with adjustments for non-direct flight paths, taxi time, and other route factors.

2. Aircraft-specific fuel consumption data for the distance traveled, including different consumption rates during various flight phases.

3. Passenger load factors based on typical occupancy rates for the specific route type.

4. Conversion of fuel consumption to CO2 emissions using a factor of 3.16 kg CO2 per kg of jet fuel, with an applied radiative forcing factor (typically 1.9) for high-altitude emissions.

Sources
-------

The following sources inform our flight emissions calculations:

1. Aircraft fuel consumption data and standardized approach for calculating flight emissions is provided by the International Civil Aviation Organization (see `ICAO Carbon Emissions Calculator <https://applications.icao.int/icec/Methodology%20ICAO%20Carbon%20Emissions%20Calculator_v13_Final.pdf>`_).

2. Comprehensive database of airports with coordinates and IATA codes for determining flight distances is available from the IATA Airport Database (see `OurAirports Database <https://davidmegginson.github.io/ourairports-data/airports.csv>`_).
