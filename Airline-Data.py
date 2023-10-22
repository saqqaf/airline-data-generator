import random
import string
import pandas as pd
from faker import Faker
import uuid

fake = Faker()

# Load airport, airline, and aircraft data from a CSV file into a DataFrame
airport_data_df = pd.read_csv('Airline-Data/source/airports.csv')
airline_data_df = pd.read_csv('Airline-Data/source/airlines.csv')
aircraft_data_df = pd.read_csv('Airline-Data/source/aircrafts.csv')


# Select the needed columns and remove rows where "name" is equal to "N/A"
airport_data_df = airport_data_df[['iata_code', 'name', 'city', 'country', 'lat_decimal', 'lon_decimal']]
airport_data_df = airport_data_df[airport_data_df['name'] != 'N/A']

# Define the number of rows for each table
num_airports = 1000
num_airlines = 50
num_aircrafts = 244 #don't change this one
num_customers = 5000000
num_flights = 100000
num_booking_data = 275000
num_booking_cancelled = 10000
num_performance_data = 12000
num_maintenance_events = 10000
num_technician_data = 500



# Function to generate a random airport row
def generate_random_airport():
    return airport_data_df.sample().iloc[0]

def generate_random_airline():
    return airline_data_df.sample().iloc[0]

# Generate AirportData
airport_data = []
for _ in range(num_airports):
    airport = generate_random_airport()
    airport_code = airport['iata_code']
    airport_name = airport['name']
    city = airport['city']
    country = airport['country']
    latitude = airport['lat_decimal']
    longitude = airport['lon_decimal']
    airport_data.append([airport_code, airport_name, city, country, latitude, longitude])



# Generate Airline
airline_data = []
for _ in range(num_airlines):
    airline = generate_random_airline()
    airline_code = airline['ICAO']
    airline_name = airline['NAME']
    airline_country = airline['Country']
    airline_data.append([airline_code, airline_name, airline_country])



# Generate AircraftData
aircraft_data = []
for i in range(num_aircrafts):
    aircraft_id = uuid.uuid4().hex[:10]
    aircraft_name = aircraft_data_df.iloc[i, 0] #I added +1 to skip the columns header row
    model = aircraft_data_df.iloc[i, 0]
    tail_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    airline_code = random.choice(airline_data)[0]
    aircraft_data.append([aircraft_id, aircraft_name, model, tail_number, airline_code])

# Generate CustomerData
customer_data = []
for _ in range(num_customers):
    customer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    customer_name = fake.name()
    loyalty_status = random.choice(['Gold', 'Silver', 'Bronze', 'None'])
    customer_segment = random.choice(['Frequent Traveler', 'Leisure Traveler', 'Business Traveler'])
    customer_data.append([customer_id, customer_name, loyalty_status, customer_segment])

# Generate FlightData
flight_data = []
for _ in range(num_flights):
    flight_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    flight_date = fake.date_between(start_date='-1y', end_date='+1y')
    origin_airport_code = random.choice(airport_data)[0]
    destination_airport_code = random.choice(airport_data)[0]
    departure_time = fake.time_object(end_datetime=None)
    arrival_time = fake.time_object(end_datetime=None)
    aircraft_id = random.choice(aircraft_data)[0]
    passenger_count = random.randint(50, 300)
    flight_data.append([flight_number, flight_date, origin_airport_code, destination_airport_code, departure_time, arrival_time, aircraft_id, passenger_count])

# Generate PerformanceData
performance_data = []
for _ in range(num_performance_data):
    flight_number = random.choice(flight_data)[0]
    departure_delay = random.randint(-30, 180)
    arrival_delay = random.randint(-30, 180)
    performance_data.append([flight_number, departure_delay, arrival_delay])

# Generate FuelConsumption
fuel_consumption = []
for flight in flight_data:
    flight_number = flight[0]
    fuel_consumed = round(random.uniform(1000, 5000), 2)
    fuel_type = random.choice(['Jet A', 'Jet B', 'Avgas'])
    fuel_consumption.append([flight_number, fuel_consumed, fuel_type])

# Generate BookingData
booking_data = []

for flight in flight_data:
    num_bookings = random.randint(10, 50)  # Generate between 1 to 5 bookings for each flight
    customer_ids_used = set()  # To track customer IDs already used in this flight
    for _ in range(num_bookings):
        # Ensure the customer ID is not a duplicate
        customer_id = None
        while customer_id is None or customer_id in customer_ids_used:
            customer_id = random.choice(customer_data)[0]

        booking_id = uuid.uuid4().hex[:10]
        booking_date = fake.date_between(start_date='-1y', end_date='today')
        customer_ids_used.add(customer_id)  # Mark the customer ID as used
        flight_number = flight[0]  # Use the flight number from the flight_data
        channel_name = random.choice(['Website', 'Mobile App', 'Travel Agent', 'Call Center'])
        revenue_amount = random.randint(100, 1000)
        booking_data.append([booking_id, booking_date, customer_id, flight_number, channel_name, revenue_amount])



# Generate BookingCancelled
booking_cancelled = []
for _ in range(num_booking_cancelled):
    cancellation_id = uuid.uuid4().hex[:10]
    booking_id = random.choice(booking_data)[0]
    cancellation_date = fake.date_between(start_date='-1y', end_date='today')
    booking_cancelled.append([cancellation_id, booking_id, cancellation_date])



# Generate MaintenanceType
event_types = [
    'Scheduled Maintenance',
    'Unscheduled Maintenance',
    'Emergency Maintenance',
    'Routine Inspection',
    'Engine Overhaul',
    'Avionics Repair',
    'Tire Replacement',
    'Painting',
    'Interior Refurbishment',
    'Landing Gear Inspection',
    'Wing Maintenance',
    'Fuel System Check',
    'Navigation System Calibration',
    'Hydraulic System Service',
    'Electrical System Repair',
    'Aircraft Cleaning',
    'Cabin Crew Training',
    'Oxygen System Check',
    'Emergency Evacuation Drill',
    'Aircraft Modification',
    'Weather Radar Calibration',
    'Aircraft Interior Cleaning',
    'Exterior Painting',
    'Cargo Handling System Service',
    'Emergency Lighting Test',
    'Aircraft Weight and Balance Check',
    'Emergency Slide Deployment Test',
    'Cockpit Instrument Calibration',
    'Engine Run-Up Test',
    'Winglet Inspection',
    'Rudder Adjustment',
    'Thrust Reverser Check',
    'Aircraft De-icing',
    'Lavatory System Service',
    'Emergency Landing Gear Deployment',
    'Engine Fan Blade Inspection',
    'Aircraft Decontamination',
    'Emergency Oxygen Mask Test',
    'Wing Flap Adjustment',
    'Aircraft Pressurization Check',
    'Cabin Air Quality Test',
    'Galley Equipment Maintenance',
    'Aircraft Water System Service',
    'Emergency Escape Slide Service',
    'Cargo Compartment Inspection',
    'Life Vest Inspection',
    'Aircraft Tire Pressure Check',
    'Security Inspection',
    'Aircraft Seating Maintenance'
]
maintenance_type = []
for _ in range(event_types):
    maintenance_type_id = uuid.uuid4().hex[:10]
    event_type = random.choice(event_types)
    description = fake.sentence(nb_words=random.randint(10, 20))
    expected_duration = random.randint(1, 120)
    maintenance_type.append([maintenance_type_id, event_type, description, expected_duration])

# Generate TechnicianData
technician_data = []
for _ in range(num_technician_data):
    technician_id = uuid.uuid4().hex[:10]
    technician_name = fake.name()
    maintenance_team = random.choice(['Team A', 'Team B', 'Team C'])
    technician_data.append([technician_id, technician_name, maintenance_team])

# Generate MaintanenceEvent
maintanence_event = []
for _ in range(num_maintenance_events):
    event_id = uuid.uuid4().hex[:10]
    event_date = fake.date_between(start_date='-1y', end_date='today')
    aircraft_id = random.choice(aircraft_data)[0]
    technician_id = random.choice(technician_data)[0]
    maintenance_type_id = random.choice(maintenance_type)[0]
    downtime_duration = random.randint(1, 48)
    maintenance_cost = round(random.uniform(1000, 10000), 2)
    maintanence_event.append([event_id, event_date, aircraft_id, technician_id, maintenance_type_id, downtime_duration, maintenance_cost])







# Convert your generated data into DataFrames
airport_df = pd.DataFrame(airport_data, columns=['iata_code', 'name', 'city', 'country', 'lat_decimal', 'lon_decimal'])
airline_df = pd.DataFrame(airline_data, columns=['airline_code', 'airline_name','airline_country'])
aircraft_df = pd.DataFrame(aircraft_data, columns=['aircraft_id', 'aircraft_name', 'model', 'tail_number', 'airline_code'])
customer_df = pd.DataFrame(customer_data, columns=['customer_id', 'customer_name', 'loyalty_status', 'customer_segment'])
flight_df = pd.DataFrame(flight_data, columns=['flight_number', 'flight_date', 'origin_airport_code', 'destination_airport_code', 'departure_time', 'arrival_time', 'aircraft_id', 'passenger_count'])
performance_df = pd.DataFrame(performance_data, columns=['flight_number', 'departure_delay', 'arrival_delay'])
fuel_consumption_df = pd.DataFrame(fuel_consumption, columns=['flight_number', 'fuel_consumed', 'fuel_type'])
booking_data_df = pd.DataFrame(booking_data, columns=['booking_id', 'booking_date', 'customer_id', 'flight_number', 'channel_name', 'revenue_amount'])
booking_cancelled_df = pd.DataFrame(booking_cancelled, columns=['cancellation_id', 'booking_id', 'cancellation_date'])
maintenance_type_df = pd.DataFrame(maintenance_type, columns=['maintenance_type_id', 'event_type', 'description', 'expected_duration'])
maintanence_event_df = pd.DataFrame(maintanence_event, columns=['event_id', 'event_date', 'aircraft_id', 'technician_id', 'maintenance_type_id', 'downtime_duration', 'maintenance_cost'])
technician_data_df = pd.DataFrame(technician_data, columns=['technician_id', 'technician_name', 'maintenance_team'])

# Save DataFrames as CSV files
airport_df.to_csv('airport.csv', index=False)
airline_df.to_csv('airline.csv', index=False)
aircraft_df.to_csv('aircraft.csv', index=False)
customer_df.to_csv('customer.csv', index=False)
flight_df.to_csv('flight.csv', index=False)
performance_df.to_csv('performance.csv', index=False)
fuel_consumption_df.to_csv('fuel_consumption.csv', index=False)
booking_data_df.to_csv('booking.csv', index=False)
booking_cancelled_df.to_csv('booking_cancelled.csv', index=False)
maintenance_type_df.to_csv('maintenance_type.csv', index=False)
maintanence_event_df.to_csv('maintenance_event.csv', index=False)
technician_data_df.to_csv('technician.csv', index=False)
