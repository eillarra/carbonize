===========================
Train emissions calculator
===========================

The Train calculator estimates carbon emissions from rail travel based on distance and train type.

Usage
-----

.. code-block:: python

    from carbonize.calculators.trains import Train

    step = Train(
        distance=250,  # km
        train_type="intercity"
    )

    print(f"Carbon footprint per passenger: {step.co2e_pax} kg CO2e")

Supported train types
--------------------

- ``local``: 0.0369 kg CO2e/km
- ``intercity``: 0.0354 kg CO2e/km
- ``highspeed``: 0.0042 kg CO2e/km
- ``underground``: 0.0275 kg CO2e/km
- ``tram``: 0.0302 kg CO2e/km

Methodology
-----------

The calculation estimates carbon emissions based on:

1. The distance traveled measured in kilometers.

2. The selected train type and its corresponding emission factor.

3. Emission factors expressed per passenger-kilometer, which incorporate average occupancy rates for each train type.

4. Total emissions calculated by multiplying the distance by the appropriate emission factor for the selected train type.

Sources
-------

The following sources inform our train emissions calculations:

1. Data on emission factors for different types of rail transport is provided by the UK Department for Environment, Food and Rural Affairs (see `DEFRA Greenhouse Gas Conversion Factors 2022 <https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2022>`_).

Note: Emission factors are based on UK rail systems and may vary in other countries depending on the electricity generation mix and specific train technologies used.
