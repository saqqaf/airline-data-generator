import random
from faker import Faker
import psycopg2
import uuid
import datetime

fake = Faker()

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

print("Created connection!")


# Function to generate a random airport code from the existing Airport table
def generate_random_airport_code():
    cursor.execute("SELECT airport_id FROM Airport limit 1000")
    airport_codes = [row[0] for row in cursor.fetchall()]
    return random.choice(airport_codes)

# Function to generate a random aircraft ID from the existing Aircraft table
def generate_random_aircraft_id():
    cursor.execute("SELECT aircraft_id FROM Aircraft limit 1000")
    aircraft_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(aircraft_ids)

# Function to generate a random customer ID from the existing Customer table
def generate_random_customer_id():
    cursor.execute("SELECT customer_id FROM Customer limit 8000")
    customer_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(customer_ids)

# Function to generate a random technician ID from the existing Customer table
def generate_random_technician_id():
    cursor.execute("SELECT technician_id FROM techniciandata limit 1000")
    technician_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(technician_ids)

# Function to generate a random maintenance_type ID from the existing Customer table
def generate_random_maintenance_type_id():
    cursor.execute("SELECT maintenance_type_id FROM maintenancetype limit 49")
    maintenance_type_ids = [row[0] for row in cursor.fetchall()]
    return random.choice(maintenance_type_ids)

conn.commit()

print("Finished fetching current data!")
# Generate FlightData
num_flights = 500  # Define the number of flights to generate
flight_data = []
for _ in range(num_flights):
    flight_number = uuid.uuid4().hex[:10]
    flight_date = fake.date_between(start_date='-1d', end_date='today')
    origin_airport_code = generate_random_airport_code()
    destination_airport_code = generate_random_airport_code()
    departure_time = fake.time_object(end_datetime=None)
    arrival_time = fake.time_object(end_datetime=None)
    aircraft_id = generate_random_aircraft_id()
    passenger_count = random.randint(50, 300)
    flight_data.append([flight_number, flight_date, origin_airport_code, destination_airport_code, departure_time, arrival_time, aircraft_id, passenger_count])

# Generate BookingData
booking_data = []
for flight in flight_data:
    num_bookings = random.randint(10, 50)
    for _ in range(num_bookings):
        customer_id = generate_random_customer_id()
        booking_id = uuid.uuid4().hex[:10]
        booking_date = fake.date_between(start_date='-1d', end_date='today')
        flight_number = flight[0]
        channel_name = random.choice(['Website', 'Mobile App', 'Travel Agent', 'Call Center'])
        revenue_amount = random.randint(100, 1000)
        booking_data.append([booking_id, booking_date, customer_id, flight_number, channel_name, revenue_amount])

# Generate BookingCancelled
booking_cancelled = []
for _ in range(10):  # Define the number of cancellations to generate
    cancellation_id = uuid.uuid4().hex[:10]
    booking_id = random.choice(booking_data)[0]
    cancellation_date = fake.date_between(start_date='-1y', end_date='today')
    booking_cancelled.append([cancellation_id, booking_id, cancellation_date])

# Generate PerformanceData
performance_data = []
for flight in flight_data:
    flight_number = flight[0]
    departure_delay = random.randint(1, 180)
    arrival_delay = random.randint(1, 180)
    performance_data.append([flight_number, departure_delay, arrival_delay])

# Generate MaintenanceEvent
maintenance_event = []
for _ in range(10):  # Define the number of maintenance events to generate
    event_id = uuid.uuid4().hex[:10]
    event_date = fake.date_between(start_date='-1d', end_date='today')
    aircraft_id = generate_random_aircraft_id()
    technician_id = generate_random_technician_id()
    maintenance_type_id = generate_random_maintenance_type_id()
    downtime_duration = random.randint(1, 164)
    maintenance_cost = round(random.uniform(1000, 10000), 2)
    maintenance_event.append([event_id, event_date, aircraft_id, technician_id, maintenance_type_id, downtime_duration, maintenance_cost])

print("Finished generating data! \n Starting inserting data!")

#------------------------------- INGESTING NEW DATA INTO DATABASE --------------------------------------------------#



# Insert the generated data into the respective tables

# Insert flight data into the Flight table
insert_flight_query = """
INSERT INTO Flight (flight_number, flight_date, origin_airport_code, destination_airport_code, departure_time, arrival_time, aircraft_id, passenger_count)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_flight_query, flight_data)

# Insert booking data into the BookingData table
insert_booking_query = """
INSERT INTO BookingData (booking_id, booking_date, customer_id, flight_number, channel_name, revenue_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_booking_query, booking_data)

# Insert booking cancellation data into the BookingCancelled table
insert_cancellation_query = """
INSERT INTO BookingCancelled (cancellation_id, booking_id, cancellation_date)
VALUES (%s, %s, %s)
"""

cursor.executemany(insert_cancellation_query, booking_cancelled)

# Insert performance data into the Performance table
insert_performance_query = """
INSERT INTO Performance (flight_number, departure_delay, arrival_delay)
VALUES (%s, %s, %s)
"""

cursor.executemany(insert_performance_query, performance_data)

# Insert maintenance event data into the MaintenanceEvent table
insert_maintenance_query = """
INSERT INTO MaintenanceEvent (event_id, event_date, aircraft_id, technician_id, maintenance_type_id, downtime_duration, maintenance_cost)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_maintenance_query, maintenance_event)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

print("Data inserted!")