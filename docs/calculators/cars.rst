=============================
Car ride emissions calculator
=============================

The Ride calculator estimates carbon emissions from car travel based on distance and vehicle type.

Usage
-----

.. code-block:: python

    from carbonize.calculators.cars import Ride

    step = Ride(
        distance=100,  # km
        vehicle_type="medium-plugin-hybrid-car",
        passengers=2   # number of people in vehicle
    )

    print(f"Carbon footprint per passenger: {step.co2e_pax} kg CO2e")

Supported vehicle types
-----------------------

- ``small-diesel-car``: 0.142 kg CO2e/km
- ``small-petrol-car``: 0.154 kg CO2e/km
- ``small-plugin-hybrid-car``: 0.073 kg CO2e/km
- ``small-electric-car``: 0.027 kg CO2e/km
- ``medium-diesel-car``: 0.171 kg CO2e/km
- ``medium-petrol-car``: 0.192 kg CO2e/km
- ``medium-plugin-hybrid-car``: 0.11 kg CO2e/km
- ``medium-electric-car``: 0.073 kg CO2e/km
- ``large-diesel-car``: 0.209 kg CO2e/km
- ``large-petrol-car``: 0.282 kg CO2e/km
- ``large-plugin-hybrid-car``: 0.126 kg CO2e/km
- ``large-electric-car``: 0.073 kg CO2e/km
- ``bus``: 0.089 kg CO2e/km
- ``bike``: 0 kg CO2e/km (zero emissions) 🚴

Methodology
-----------

The calculation estimates carbon emissions based on:

1. The distance traveled measured in kilometers.

2. Vehicle type parameters including fuel type (petrol, diesel, hybrid, electric), vehicle size (small, medium, large), and well-to-wheel emissions covering both fuel production and combustion.

3. Number of passengers in the vehicle.

4. Total emissions calculated by multiplying the distance by the emission factor for the selected vehicle type, with per-passenger emissions derived by dividing this total by the number of passengers.

Sources
-------

The following sources inform our car emissions calculations:

1. Detailed emission factors for different transport modes are provided by the UK Department for Environment, Food and Rural Affairs (see `DEFRA Greenhouse Gas Conversion Factors 2022 <https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2022>`_).

2. Data for various vehicle classes, sizes, and fuel types is available in the European Environment Agency's COPERT methodology (see `EEA EMEP/EEA Guidebook <https://www.eea.europa.eu/publications/emep-eea-guidebook-2019/part-b-sectoral-guidance-chapters/1-energy/1-a-combustion/1-a-3-b-i/view>`_).

3. Methodologies for estimating emissions from transportation are detailed in the Intergovernmental Panel on Climate Change Guidelines (see `IPCC Guidelines for National Greenhouse Gas Inventories <https://www.ipcc-nggip.iges.or.jp/public/2019rf/index.html>`_).

Note: The emission factors used in this calculator represent average values that may vary depending on specific vehicle models, driving conditions, and regional electricity grid mixes (for electric vehicles).
