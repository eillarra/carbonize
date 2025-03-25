from carbonize import Footprint


# Create a footprint with multiple emission sources
footprint = Footprint()

# Add a one-way flight
footprint.add_flight(a="LHR", b="JFK")

# Add a car ride with 2 passengers
footprint.add_ride(distance=50, vehicle_type="medium-petrol-car", passengers=2)

# Add a return train journey
footprint.add_train(distance=200, train_type="highspeed", two_way=True)

# Add a webinar attendance
footprint.add_webinar(duration=60, device_type="laptop", video_quality="hd")

# Get the total emissions
total = footprint.co2e
print(f"Total carbon footprint: {total} kg CO2e")
