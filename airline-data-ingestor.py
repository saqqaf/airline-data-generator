import random
import string
import pandas as pd
from faker import Faker
import uuid
import psycopg2  

print("Geneating data started!")

fake = Faker()

# Functions to generate data with some data issues
# Function to introduce missing data
def introduce_missing_data(value, probability=0.01):
    return "NaN" if random.random() < probability else value

# Function to introduce outliers
def introduce_outliers(value, probability=0.01):
    if random.random() < probability:
        return value * random.uniform(10, 40)  # Increase the value significantly
    return value

# Function to introduce typos
def introduce_typos(value, probability=0.0005):
    if random.random() < probability and isinstance(value, str):
        chars = list(value)
        random_index = random.randint(0, len(chars) - 1)
        chars[random_index] = random.choice(string.ascii_letters + string.digits)
        return ''.join(chars)
    return value


# Load airport, airline, and aircraft data from a CSV file into a DataFrame
airport_data_df = pd.read_csv('/app/airports.csv')
airline_data_df = pd.read_csv('/app/airlines.csv')
aircraft_data_df = pd.read_csv('/app/aircrafts.csv')

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
    airport_id = uuid.uuid4().hex[:6]
    airport_code = airport['iata_code']
    airport_name = airport['name']
    city = airport['city']
    country = airport['country']
    latitude = airport['lat_decimal']
    longitude = airport['lon_decimal']
    airport_data.append([airport_id, airport_code, airport_name, city, country, latitude, longitude])




# Generate Airline
airline_data = []
for _ in range(num_airlines):
    airline = generate_random_airline()
    airline_id = uuid.uuid4().hex[:10]
    airline_code = airline['ICAO']
    airline_name = airline['NAME']
    airline_country = airline['Country']
    airline_data.append([airline_id, airline_code, airline_name, airline_country])



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
    loyalty_status = introduce_missing_data(random.choice(['Gold', 'Silver', 'Bronze', 'None']))
    customer_segment = introduce_missing_data(random.choice(['Frequent Traveler', 'Leisure Traveler', 'Business Traveler']))
    customer_data.append([customer_id, customer_name, loyalty_status, customer_segment])

# Generate FlightData
flight_data = []
for _ in range(num_flights):
    flight_number = uuid.uuid4().hex[:10] #''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    flight_date = fake.date_between(start_date='-1y', end_date='today')
    origin_airport_code = random.choice(airport_data)[0]
    destination_airport_code = random.choice(airport_data)[0]
    departure_time = fake.time_object(end_datetime=None)
    arrival_time = fake.time_object(end_datetime=None)
    aircraft_id = random.choice(aircraft_data)[0]
    #passenger_count = random.randint(50, 300)
    flight_data.append([flight_number, flight_date, origin_airport_code, destination_airport_code, departure_time, arrival_time, aircraft_id])

# Generate PerformanceData
performance_data = []
for _ in range(num_performance_data):
    flight_number = random.choice(flight_data)[0]
    departure_delay = random.randint(1, 180)
    arrival_delay = random.randint(1, 180)
    performance_data.append([flight_number, departure_delay, arrival_delay])

# Generate FuelConsumption
fuel_consumption = []
for flight in flight_data:
    flight_number = flight[0]
    fuel_consumed = round(random.uniform(1000, 5000), 2)
    fuel_type = introduce_missing_data(introduce_typos(random.choice(['Jet A', 'Jet B', 'Avgas'])))
    fuel_consumption.append([flight_number, fuel_consumed, fuel_type])

# Generate BookingData
booking_data = []

for flight in flight_data:
    num_bookings = random.randint(10, 250)  # Generate between 1 to 5 bookings for each flight
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
        channel_name = introduce_missing_data(introduce_typos(random.choice(['Website', 'Mobile App', 'Travel Agent', 'Call Center'])))
        revenue_amount = introduce_outliers(random.randint(100, 1000))
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
for i in event_types:
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
    maintenance_team = introduce_typos(random.choice(['Team A', 'Team B', 'Team C', 'Team D']))
    technician_data.append([technician_id, technician_name, maintenance_team])

# Generate MaintanenceEvent
maintanence_event = []
for _ in range(num_maintenance_events):
    event_id = uuid.uuid4().hex[:10]
    event_date = fake.date_between(start_date='-1y', end_date='today')
    aircraft_id = random.choice(aircraft_data)[0]
    technician_id = random.choice(technician_data)[0]
    maintenance_type_id = random.choice(maintenance_type)[0]
    downtime_duration = introduce_outliers(random.randint(1, 48))
    maintenance_cost = introduce_outliers(round(random.uniform(1000, 10000), 2))
    maintanence_event.append([event_id, event_date, aircraft_id, technician_id, maintenance_type_id, downtime_duration, maintenance_cost])







# Convert your generated data into DataFrames
airport_df = pd.DataFrame(airport_data, columns=['airport_id','iata_code', 'name', 'city', 'country', 'lat_decimal', 'lon_decimal'])
airline_df = pd.DataFrame(airline_data, columns=['airline_id', 'airline_code', 'airline_name','airline_country'])
aircraft_df = pd.DataFrame(aircraft_data, columns=['aircraft_id', 'aircraft_name', 'model', 'tail_number', 'airline_id'])
customer_df = pd.DataFrame(customer_data, columns=['customer_id', 'customer_name', 'loyalty_status', 'customer_segment'])
flight_df = pd.DataFrame(flight_data, columns=['flight_number', 'flight_date', 'origin_airport_code', 'destination_airport_code', 'departure_time', 'arrival_time', 'aircraft_id'])
performance_df = pd.DataFrame(performance_data, columns=['flight_number', 'departure_delay', 'arrival_delay'])
fuel_consumption_df = pd.DataFrame(fuel_consumption, columns=['flight_number', 'fuel_consumed', 'fuel_type'])
booking_data_df = pd.DataFrame(booking_data, columns=['booking_id', 'booking_date', 'customer_id', 'flight_number', 'channel_name', 'revenue_amount'])
booking_cancelled_df = pd.DataFrame(booking_cancelled, columns=['cancellation_id', 'booking_id', 'cancellation_date'])
maintenance_type_df = pd.DataFrame(maintenance_type, columns=['maintenance_type_id', 'event_type', 'description', 'expected_duration'])
maintanence_event_df = pd.DataFrame(maintanence_event, columns=['event_id', 'event_date', 'aircraft_id', 'technician_id', 'maintenance_type_id', 'downtime_duration', 'maintenance_cost'])
technician_data_df = pd.DataFrame(technician_data, columns=['technician_id', 'technician_name', 'maintenance_team'])







#-------------------------------- DATABASE CREDINTALS ------------------------------ #

# Define your PostgreSQL database credentials
db_credentials = {
    'dbname': 'saqqaf_airlines',
    'user': 'postgres',
    'password': 'admin',
    'host': '192.168.100.10',
    'port': '5443'
}



# Create a connection to the PostgreSQL database
conn = psycopg2.connect(**db_credentials)
cursor = conn.cursor()


#----------------------------------------------------------- CREATING TABLES ----------------------------------------------------#

# Create the Airport table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Airport (
   airport_id VARCHAR(6) PRIMARY KEY,
   iata_code VARCHAR(3),
   name VARCHAR(255),
   city VARCHAR(255),
   country VARCHAR(255),
   lat_decimal FLOAT,
   lon_decimal FLOAT
)
""")


# Create the Airline table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Airline (
   airline_id VARCHAR(10) PRIMARY KEY,
   airline_code VARCHAR(10),
   airline_name VARCHAR(255),
   airline_country VARCHAR(255)
)
""")

# Create the Aircraft table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Aircraft (
   aircraft_id VARCHAR(10) PRIMARY KEY,
   aircraft_name VARCHAR(255),
   model VARCHAR(255),
   tail_number VARCHAR(6),
   airline_id VARCHAR(10),
   FOREIGN KEY (airline_id) REFERENCES Airline (airline_id)
)
""")


# Create the Customer table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
   customer_id VARCHAR(10) PRIMARY KEY,
   customer_name VARCHAR(255),
   loyalty_status VARCHAR(10),
   customer_segment VARCHAR(255)
)
""")

# Create the Flight table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight (
   flight_number VARCHAR(10) PRIMARY KEY,
   flight_date DATE,
   origin_airport_code VARCHAR(6),
   destination_airport_code VARCHAR(6),
   departure_time TIME,
   arrival_time TIME,
   aircraft_id VARCHAR(10),
   FOREIGN KEY (origin_airport_code) REFERENCES Airport (airport_id),
   FOREIGN KEY (destination_airport_code) REFERENCES Airport (airport_id),
   FOREIGN KEY (aircraft_id) REFERENCES Aircraft (aircraft_id)
)
""")

# Create the Performance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Performance (
   flight_number VARCHAR(10),
   departure_delay INTEGER,
   arrival_delay INTEGER
)
""")

# Create the FuelConsumption table
cursor.execute("""
CREATE TABLE IF NOT EXISTS FuelConsumption (
   flight_number VARCHAR(10),
   fuel_consumed NUMERIC(8, 2),
   fuel_type VARCHAR(10)
)
""")

# Create the BookingData table
cursor.execute("""
CREATE TABLE IF NOT EXISTS BookingData (
   booking_id VARCHAR(10) PRIMARY KEY,
   booking_date DATE,
   customer_id VARCHAR(10),
   flight_number VARCHAR(10),
   channel_name VARCHAR(255),
   revenue_amount NUMERIC(10, 2),
   FOREIGN KEY (customer_id) REFERENCES Customer (customer_id),
   FOREIGN KEY (flight_number) REFERENCES Flight (flight_number)
)
""")

# Create the BookingCancelled table
cursor.execute("""
CREATE TABLE IF NOT EXISTS BookingCancelled (
   cancellation_id VARCHAR(10) PRIMARY KEY,
   booking_id VARCHAR(10),
   cancellation_date DATE,
   FOREIGN KEY (booking_id) REFERENCES BookingData (booking_id)
)
""")




# Create the MaintenanceType table
cursor.execute("""
CREATE TABLE IF NOT EXISTS MaintenanceType (
   maintenance_type_id VARCHAR(10) PRIMARY KEY,
   event_type VARCHAR(255),
   description TEXT,
   expected_duration INTEGER
)
""")

# Create the TechnicianData table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TechnicianData (
   technician_id VARCHAR(10) PRIMARY KEY,
   technician_name VARCHAR(255),
   maintenance_team VARCHAR(255)
)
""")

# Create the MaintenanceEvent table
cursor.execute("""
CREATE TABLE IF NOT EXISTS MaintenanceEvent (
   event_id VARCHAR(10) PRIMARY KEY,
   event_date DATE,
   aircraft_id VARCHAR(10),
   technician_id VARCHAR(10),
   maintenance_type_id VARCHAR(10),
   downtime_duration INTEGER,
   maintenance_cost NUMERIC(10, 2),
   FOREIGN KEY (aircraft_id) REFERENCES Aircraft (aircraft_id),
   FOREIGN KEY (technician_id) REFERENCES TechnicianData (technician_id),
   FOREIGN KEY (maintenance_type_id) REFERENCES MaintenanceType (maintenance_type_id)
)
""")


# Commit the table creations
conn.commit()



#------------------------------------ INSERTING DATA ---------------------------------#

# Insert data into the Airport table
for _, row in airport_df.iterrows():
    cursor.execute("""
    INSERT INTO Airport (airport_id, iata_code, name, city, country, lat_decimal, lon_decimal)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['airport_id'], row['iata_code'], row['name'], row['city'], row['country'], row['lat_decimal'], row['lon_decimal']))

# Insert data into the Airline table
for _, row in airline_df.iterrows():
    cursor.execute("""
    INSERT INTO Airline (airline_id, airline_code, airline_name, airline_country)
    VALUES (%s, %s, %s, %s)
    """, (row['airline_id'], row['airline_code'], row['airline_name'], row['airline_country']))

# Insert data into the Aircraft table
for _, row in aircraft_df.iterrows():
    cursor.execute("""
    INSERT INTO Aircraft (aircraft_id, aircraft_name, model, tail_number, airline_id)
    VALUES (%s, %s, %s, %s, %s)
    """, (row['aircraft_id'], row['aircraft_name'], row['model'], row['tail_number'], row['airline_id']))



# Insert data into the Customer table
for _, row in customer_df.iterrows():
    cursor.execute("""
    INSERT INTO Customer (customer_id, customer_name, loyalty_status, customer_segment)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (customer_id) DO NOTHING
    """, (row['customer_id'], row['customer_name'], row['loyalty_status'], row['customer_segment']))

# Insert data into the Flight table
for _, row in flight_df.iterrows():
    cursor.execute("""
    INSERT INTO Flight (flight_number, flight_date, origin_airport_code, destination_airport_code, departure_time, arrival_time, aircraft_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['flight_number'], row['flight_date'], row['origin_airport_code'], row['destination_airport_code'], row['departure_time'], row['arrival_time'], row['aircraft_id']))

# Insert data into the Performance table
for _, row in performance_df.iterrows():
    cursor.execute("""
    INSERT INTO Performance (flight_number, departure_delay, arrival_delay)
    VALUES (%s, %s, %s)
    """, (row['flight_number'], row['departure_delay'], row['arrival_delay']))

# Insert data into the FuelConsumption table
for _, row in fuel_consumption_df.iterrows():
    cursor.execute("""
    INSERT INTO FuelConsumption (flight_number, fuel_consumed, fuel_type)
    VALUES (%s, %s, %s)
    """, (row['flight_number'], row['fuel_consumed'], row['fuel_type']))

# Insert data into the BookingData table
for _, row in booking_data_df.iterrows():
    cursor.execute("""
    INSERT INTO BookingData (booking_id, booking_date, customer_id, flight_number, channel_name, revenue_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (booking_id) DO NOTHING
    """, (row['booking_id'], row['booking_date'], row['customer_id'], row['flight_number'], row['channel_name'], row['revenue_amount']))

# Insert data into the BookingCancelled table
for _, row in booking_cancelled_df.iterrows():
    cursor.execute("""
    INSERT INTO BookingCancelled (cancellation_id, booking_id, cancellation_date)
    VALUES (%s, %s, %s)
    ON CONFLICT (cancellation_id) DO NOTHING
    """, (row['cancellation_id'], row['booking_id'], row['cancellation_date']))

# Insert data into the MaintenanceType table
for _, row in maintenance_type_df.iterrows():
    cursor.execute("""
    INSERT INTO MaintenanceType (maintenance_type_id, event_type, description, expected_duration)
    VALUES (%s, %s, %s, %s)
    """, (row['maintenance_type_id'], row['event_type'], row['description'], row['expected_duration']))

# Insert data into the TechnicianData table
for _, row in technician_data_df.iterrows():
    cursor.execute("""
    INSERT INTO TechnicianData (technician_id, technician_name, maintenance_team)
    VALUES (%s, %s, %s)
    """, (row['technician_id'], row['technician_name'], row['maintenance_team']))

# Insert data into the MaintenanceEvent table
for _, row in maintanence_event_df.iterrows():
    cursor.execute("""
    INSERT INTO MaintenanceEvent (event_id, event_date, aircraft_id, technician_id, maintenance_type_id, downtime_duration, maintenance_cost)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING
    """, (row['event_id'], row['event_date'], row['aircraft_id'], row['technician_id'], row['maintenance_type_id'], row['downtime_duration'], row['maintenance_cost']))



# Commit and close the connection
conn.commit()
cursor.close()
conn.close()