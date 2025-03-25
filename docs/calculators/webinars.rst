============================
Webinar emissions calculator
============================

The webinar calculators estimate carbon emissions from online video conferencing and virtual events, with separate calculators for attending and hosting webinars.

Attending a webinar
-------------------

The ``Webinar`` calculator estimates emissions for attending an online meeting:

.. code-block:: python

    from carbonize.calculators.webinars import Webinar

    attending = Webinar(
        duration=60,              # minutes
        device_type="laptop",     # laptop, mobile, or tablet
        video_quality="standard"  # video_off, standard, or hd
    )

    print(f"Carbon footprint of attending: {attending.co2e} kg CO2e")

Hosting a webinar
-----------------

The ``HostedWebinar`` calculator estimates emissions for hosting an online meeting, including server-side emissions:

.. code-block:: python

    from carbonize.calculators.webinars import HostedWebinar

    hosting = HostedWebinar(
        duration=60,          # minutes
        participants=25,      # number of attendees including host
        device_type="laptop", # device used by the host
        video_quality="hd"    # video quality setting
    )

    print(f"Total carbon footprint of hosting: {hosting.co2e} kg CO2e")
    print(f"Per participant footprint: {hosting.co2e_pax} kg CO2e")

Supported device types
----------------------

- ``laptop``: Standard laptop or desktop computer
- ``mobile``: Smartphone
- ``tablet``: Tablet device

Video quality options
---------------------

- ``video_off``: Audio only
- ``standard``: Standard definition video
- ``hd``: High definition video

Methodology
-----------

The calculation estimates carbon emissions based on:

1. Attendee-side factors including device energy consumption, video quality settings, and participation duration.

2. Host-side factors including server infrastructure, data center energy consumption, network transmission requirements, and number of participants.

3. Processing energy at data centers, network transmission energy, and end-user device energy consumption.

Emissions comparisons
---------------------

Approximate emissions for a 1-hour meeting:

+------------------+------------------+--------------------+
| Activity         | Device & Quality | Emissions (kg CO2e)|
+==================+==================+====================+
| Attending        | Mobile, audio    | 0.04               |
+------------------+------------------+--------------------+
| Attending        | Laptop, standard | 0.15               |
+------------------+------------------+--------------------+
| Attending        | Laptop, HD       | 0.23               |
+------------------+------------------+--------------------+
| Hosting (10 pax) | Laptop, standard | 0.65 total         |
+------------------+------------------+--------------------+

Sources
-------

The following sources inform our webinar emissions calculations:

1. Data on energy usage per hour of video conferencing is provided by the Zoom Sustainability Report (see `Zoom Sustainability Report <https://blog.zoom.us/how-video-meetings-are-helping-reduce-environmental-impact-infographic/>`_).

2. A comprehensive analysis of streaming carbon footprints is available in the Carbon Trust's "Carbon Impact of Video Streaming" (see `Carbon Trust <https://www.carbontrust.com/resources/carbon-impact-of-video-streaming>`_).

3. Academic research on video conferencing emissions is detailed in MIT's "The energy and carbon footprints of videoconferencing" (see `MIT <https://ctl.mit.edu/sites/default/files/inline-files/Videoconferencing%20Footprint%20Taddei%26Menefee.pdf>`_).

4. The IEA provides an analysis of different streaming scenarios in "The Carbon Footprint of Streaming Video" (see `IEA <https://www.iea.org/commentaries/the-carbon-footprint-of-streaming-video-fact-checking-the-headlines>`_).
