==========
Quickstart
==========

Installation
------------

.. code-block:: bash

  $ pip install carbonize

Basic usage
-----------

``carbonize`` provides various calculators for different emission sources.
Each calculator is designed for a specific type of activity.

For convenience, you can use the `Footprint` class to combine emissions from multiple sources:

.. code-block:: python

    from carbonize import Footprint

    footprint = Footprint()
    footprint.add_flight(a="LHR", b="JFK")
    footprint.add_ride(distance=50, vehicle_type="medium-petrol-car", passengers=2)
    footprint.add_train(distance=200, train_type="highspeed", two_way=True)
    footprint.add_webinar(duration=60, device_type="laptop", video_quality="hd")

    total = footprint.co2e
    print(f"Total carbon footprint: {total} kg CO2e")

Available calculators
---------------------

In addition to the `Footprint` class, you can use individual calculators to calculate emissions from specific sources:

- **Flight**: calculates air travel emissions :doc:`(learn more) <calculators/flights>`
- **Ride**: calculates emissions from car and bus travel :doc:`(learn more) <calculators/cars>`
- **Train**: calculates emissions from train travel :doc:`(learn more) <calculators/trains>`
- **Webinar**: calculates emissions from online meetings :doc:`(learn more) <calculators/webinars>`
