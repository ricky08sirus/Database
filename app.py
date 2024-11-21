# import streamlit as st
# import mysql.connector
# import pandas as pd
# from mysql.connector import Error

# # Database connection
# def create_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="6394",
#             database="dbms_project"
#         )
#         return conn
#     except Error as e:
#         st.error(f"Error connecting to database: {e}")
#         return None

# # Fetch data from a table
# def fetch_data(query):
#     conn = create_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(query)
#         data = cursor.fetchall()
#         conn.close()
#         return pd.DataFrame(data) if data else pd.DataFrame()
#     else:
#         return pd.DataFrame()

# # Execute a query
# def execute_query(query, values=None):
#     conn = create_connection()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             if values:
#                 cursor.execute(query, values)
#             else:
#                 cursor.execute(query)
#             conn.commit()
#             conn.close()
#             st.success("Operation executed successfully.")
#         except Error as e:
#             st.error(f"Error executing query: {e}")
#     else:
#         st.error("Failed to execute operation.")

# # Streamlit app
# st.title("Airport Runway Management - CRUD Operations")

# # Navigation
# menu = ["Flights", "Runways", "Maintenance", "Runway Schedules", "Weather"]
# choice = st.sidebar.selectbox("Select Table", menu)

# # Flights CRUD
# if choice == "Flights":
#     st.subheader("Manage Flights")
#     operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"])

#     if operation == "Create":
#         with st.form("create_flight"):
#             flight_number = st.text_input("Flight Number")
#             airline = st.text_input("Airline")
#             status = st.selectbox("Status", ["Scheduled", "In-Flight", "Landed", "Cancelled"])
#             size = st.selectbox("Size", ["Small", "Large"])
#             scheduled_time = st.number_input("Scheduled Time", min_value=0, step=1)
#             submit = st.form_submit_button("Add Flight")

#             if submit:
#                 query = """
#                 INSERT INTO flights (Flight_Number, Airline, Status, Size, Scheduled_Time)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """
#                 execute_query(query, (flight_number, airline, status, size, scheduled_time))

#     elif operation == "Read":
#         df = fetch_data("SELECT * FROM flights")
#         st.dataframe(df)

#     elif operation == "Update":
#         flight_id = st.number_input("Enter Flight ID to Update", min_value=1, step=1)
#         column = st.selectbox("Column to Update", ["Flight_Number", "Airline", "Status", "Size", "Scheduled_Time"])
#         value = st.text_input("New Value")
#         if st.button("Update Flight"):
#             query = f"UPDATE flights SET {column} = %s WHERE Flight_ID = %s"
#             execute_query(query, (value, flight_id))

#     elif operation == "Delete":
#         flight_id = st.number_input("Enter Flight ID to Delete", min_value=1, step=1)
#         if st.button("Delete Flight"):
#             query = "DELETE FROM flights WHERE Flight_ID = %s"
#             execute_query(query, (flight_id,))

# # Runways CRUD
# elif choice == "Runways":
#     st.subheader("Manage Runways")
#     operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"])

#     if operation == "Create":
#         with st.form("create_runway"):
#             runway_name = st.text_input("Runway Name")
#             status = st.selectbox("Status", ["Available", "Occupied", "Under Maintenance", "Closed"])
#             length = st.number_input("Length", min_value=0, step=1)
#             size = st.selectbox("Size", ["Small", "Large"])
#             shutdown_weather = st.selectbox("Shutdown Weather", ["None", "Rainy", "Snowy"])
#             submit = st.form_submit_button("Add Runway")

#             if submit:
#                 query = """
#                 INSERT INTO runways (Runway_Name, Runway_Status, Length, Size, Shutdown_Weather)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """
#                 execute_query(query, (runway_name, status, length, size, shutdown_weather))

#     elif operation == "Read":
#         df = fetch_data("SELECT * FROM runways")
#         st.dataframe(df)

#     elif operation == "Update":
#         runway_id = st.number_input("Enter Runway ID to Update", min_value=1, step=1)
#         column = st.selectbox("Column to Update", ["Runway_Name", "Runway_Status", "Length", "Size", "Shutdown_Weather"])
#         value = st.text_input("New Value")
#         if st.button("Update Runway"):
#             query = f"UPDATE runways SET {column} = %s WHERE Runway_ID = %s"
#             execute_query(query, (value, runway_id))

#     elif operation == "Delete":
#         runway_id = st.number_input("Enter Runway ID to Delete", min_value=1, step=1)
#         if st.button("Delete Runway"):
#             query = "DELETE FROM runways WHERE Runway_ID = %s"
#             execute_query(query, (runway_id,))
    


# # CRUD for Maintenance
# if choice == "Maintenance":
#     st.subheader("Manage Maintenance Records")
#     operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"])

#     if operation == "Create":
#         with st.form("create_maintenance"):
#             runway_id = st.number_input("Runway ID", min_value=1, step=1)
#             description = st.text_area("Description")
#             submit = st.form_submit_button("Add Maintenance Record")

#             if submit:
#                 query = """
#                 INSERT INTO maintenance (Runway_ID, Description)
#                 VALUES (%s, %s)
#                 """
#                 execute_query(query, (runway_id, description))
#                 st.success("Maintenance record added successfully!")

#     elif operation == "Read":
#         data = fetch_data("SELECT * FROM maintenance")
#         st.dataframe(data)

#     elif operation == "Update":
#         maintenance_id = st.number_input("Enter Maintenance ID to Update", min_value=1, step=1)
#         description = st.text_area("New Description")
#         if st.button("Update Maintenance Record"):
#             query = "UPDATE maintenance SET Description = %s WHERE Maintenance_ID = %s"
#             execute_query(query, (description, maintenance_id))
#             st.success("Maintenance record updated successfully!")

#     elif operation == "Delete":
#         maintenance_id = st.number_input("Enter Maintenance ID to Delete", min_value=1, step=1)
#         if st.button("Delete Maintenance Record"):
#             query = "DELETE FROM maintenance WHERE Maintenance_ID = %s"
#             execute_query(query, (maintenance_id,))
#             st.success("Maintenance record deleted successfully!")

# # CRUD for Runway Schedules
# elif choice == "Runway Schedules":
#     st.subheader("Manage Runway Schedules")
#     operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"])

#     if operation == "Create":
#         with st.form("create_runway_schedule"):
#             runway_id = st.number_input("Runway ID", min_value=1, step=1)
#             flight_id = st.number_input("Flight ID", min_value=1, step=1)
#             scheduled_time = st.number_input("Scheduled Time (minutes past midnight)", min_value=0, step=1)
#             duration = st.number_input("Duration (minutes)", min_value=1, step=1)
#             submit = st.form_submit_button("Add Runway Schedule")

#             if submit:
#                 query = """
#                 INSERT INTO runway_schedules (Runway_ID, Flight_ID, Scheduled_Time, Duration)
#                 VALUES (%s, %s, %s, %s)
#                 """
#                 execute_query(query, (runway_id, flight_id, scheduled_time, duration))
#                 st.success("Runway schedule added successfully!")

#     elif operation == "Read":
#         data = fetch_data("SELECT * FROM runway_schedules")
#         st.dataframe(data)

#     elif operation == "Update":
#         schedule_id = st.number_input("Enter Schedule ID to Update", min_value=1, step=1)
#         column = st.selectbox("Column to Update", ["Runway_ID", "Flight_ID", "Scheduled_Time", "Duration"])
#         value = st.text_input("New Value")
#         if st.button("Update Runway Schedule"):
#             query = f"UPDATE runway_schedules SET {column} = %s WHERE Schedule_ID = %s"
#             execute_query(query, (value, schedule_id))
#             st.success("Runway schedule updated successfully!")

#     elif operation == "Delete":
#         schedule_id = st.number_input("Enter Schedule ID to Delete", min_value=1, step=1)
#         if st.button("Delete Runway Schedule"):
#             query = "DELETE FROM runway_schedules WHERE Schedule_ID = %s"
#             execute_query(query, (schedule_id,))
#             st.success("Runway schedule deleted successfully!")

# # CRUD for Weather
# elif choice == "Weather":
#     st.subheader("Manage Weather Conditions")
#     operation = st.radio("Operation", ["Read", "Update"])

#     if operation == "Read":
#         data = fetch_data("SELECT * FROM weather")
#         st.dataframe(data)

#     elif operation == "Update":
#         current_weather = st.selectbox("Set Current Weather Condition", ["Optimal", "Rainy", "Snowy"])
#         if st.button("Update Weather Condition"):
#             query = "UPDATE weather SET Current_Weather = %s"
#             execute_query(query, (current_weather,))
#             st.success(f"Weather condition updated to {current_weather}!")


# Maintenance, Runway Schedules, and Weather CRUD can be similarly implemented
# Use the same pattern for these tables as shown above.


import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="6394",
        database="dbms_project"
    )

def fetch_data(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    conn.close()
    return result

def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    conn.close()

def call_new_weather_procedure(weather_status):
    query = "CALL new_weather(%s)"
    execute_query(query, (weather_status,))

def call_schedule_flights_procedure():
    query = "CALL ScheduleFlights()"
    execute_query(query)

def get_closed_runways_count():
    query = "SELECT ClosedRunways();"
    result = fetch_data(query)
    return result[0]['ClosedRunways()'] if result else 0

st.title("Runway and Flight Management System")

menu = ["Flights", "Runways", "Maintenance", "Runway Schedules","Weather"]
choice = st.sidebar.selectbox("Select Operation", menu)

# 1. Flights Management
if choice == "Flights":
    st.subheader("Manage Flights")
    operation = st.radio("Operation", ["Create", "Read", "Update", "Delete","Schedule Flights"])

    if operation == "Create":
        with st.form("create_flight"):
            flight_number = st.text_input("Flight Number")
            airline = st.text_input("Airline")
            size = st.selectbox("Size", ["Small", "Large"])
            scheduled_time = st.number_input("Scheduled Time (HHMM)", min_value=0, max_value=2359, step=1)
            submit = st.form_submit_button("Add Flight")

            if submit:
                query = """
                INSERT INTO flights (Flight_Number, Airline, Size, Scheduled_Time)
                VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (flight_number, airline, size, scheduled_time))
                st.success(f"Flight {flight_number} added successfully!")

    elif operation == "Read":
        data = fetch_data("SELECT * FROM flights")
        st.dataframe(data)

    elif operation == "Update":
        flight_id = st.number_input("Flight ID", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Scheduled", "In-Flight", "Landed", "Cancelled"])
        if st.button("Update Flight Status"):
            query = "UPDATE flights SET Status = %s WHERE Flight_ID = %s"
            execute_query(query, (new_status, flight_id))
            st.success(f"Flight ID {flight_id} status updated to {new_status}!")

    elif operation == "Delete":
        flight_id = st.number_input("Flight ID", min_value=1, step=1)
        if st.button("Delete Flight"):
            query = "DELETE FROM flights WHERE Flight_ID = %s"
            execute_query(query, (flight_id,))
            st.success(f"Flight ID {flight_id} deleted successfully!")
    
    elif operation== "Schedule Flights":
        call_schedule_flights_procedure()
        st.success("Schedule Flights procedure executed successfully!")

# 2. Runways Management
elif choice == "Runways":
    st.subheader("Manage Runways")
    operation = st.radio("Operation", ["Create", "Read", "Update", "Delete","Closed Runways Count"])

    if operation == "Create":
        with st.form("create_runway"):
            runway_name = st.text_input("Runway Name")
            length = st.number_input("Length (in meters)", min_value=0, step=1)
            size = st.selectbox("Size", ["Small", "Large"])
            shutdown_weather = st.selectbox("Shutdown Weather", ["None", "Rainy", "Snowy"])
            submit = st.form_submit_button("Add Runway")

            if submit:
                query = """
                INSERT INTO runways (Runway_Name, Length, Size, Shutdown_Weather)
                VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (runway_name, length, size, shutdown_weather))
                st.success(f"Runway {runway_name} added successfully!")

    elif operation == "Read":
        data = fetch_data("SELECT * FROM runways")
        st.dataframe(data)

    elif operation == "Update":
        runway_id = st.number_input("Runway ID", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Available", "Occupied", "Under Maintenance", "Closed"])
        if st.button("Update Runway Status"):
            query = "UPDATE runways SET Runway_Status = %s WHERE Runway_ID = %s"
            execute_query(query, (new_status, runway_id))
            st.success(f"Runway ID {runway_id} status updated to {new_status}!")

    elif operation == "Delete":
        runway_id = st.number_input("Runway ID", min_value=1, step=1)
        if st.button("Delete Runway"):
            query = "DELETE FROM runways WHERE Runway_ID = %s"
            execute_query(query, (runway_id,))
            st.success(f"Runway ID {runway_id} deleted successfully!")
    elif operation == "Closed Runways Count":
        closed_count = get_closed_runways_count()
        st.write(f"There are {closed_count} closed runways due to rainy or snowy weather.")

# 3. Maintenance Management
elif choice == "Maintenance":
    st.subheader("Manage Maintenance")
    operation = st.radio("Operation", [ "Read", "Delete"])

    # if operation == "Create":
    #     with st.form("create_maintenance"):
    #         runway_id = st.number_input("Runway ID", min_value=1, step=1)
    #         description = st.text_area("Maintenance Description")
    #         submit = st.form_submit_button("Add Maintenance")

    #         if submit:
    #             query = """
    #             INSERT INTO maintenance (Runway_ID, Description)
    #             VALUES (%s, %s)
    #             """
    #             execute_query(query, (runway_id, description))
    #             st.success(f"Maintenance record for Runway ID {runway_id} added successfully!")

    if operation == "Read":
        data = fetch_data("SELECT * FROM maintenance")
        st.dataframe(data)

    elif operation == "Delete":
        maintenance_id = st.number_input("Maintenance ID", min_value=1, step=1)
        if st.button("Delete Maintenance Record"):
            query = "DELETE FROM maintenance WHERE Maintenance_ID = %s"
            execute_query(query, (maintenance_id,))
            st.success(f"Maintenance record ID {maintenance_id} deleted successfully!")

# 4. Runway Schedules Management
elif choice == "Runway Schedules":
    st.subheader("Manage Runway Schedules")
    operation = st.radio("Operation", ["Read", "Delete"])

    if operation == "Read":
        data = fetch_data("""
        SELECT rs.Schedule_ID, r.Runway_Name, f.Flight_Number, rs.Scheduled_Time, rs.Duration
        FROM runway_schedules rs
        JOIN runways r ON rs.Runway_ID = r.Runway_ID
        JOIN flights f ON rs.Flight_ID = f.Flight_ID
        """)
        st.dataframe(data)

    elif operation == "Delete":
        schedule_id = st.number_input("Schedule ID", min_value=1, step=1)
        if st.button("Delete Schedule"):
            query = "DELETE FROM runway_schedules WHERE Schedule_ID = %s"
            execute_query(query, (schedule_id,))
            st.success(f"Runway schedule ID {schedule_id} deleted successfully!")

# 5. Weather Management
elif choice == "Weather":
    st.subheader("Manage Weather")
    weather_menu = ["Optimal","Rainy","Snowy"]
    weather_choice = st.selectbox("Select Operation", weather_menu)
    if weather_choice:
        st.write(f"Running procedure for weather condition: {weather_choice}")
        call_new_weather_procedure(weather_choice)
        st.success(f"Procedure for '{weather_choice}' executed successfully!")

    # operation = st.radio("Operation", ["Read", "Update"])

    # if operation == "Read":
    #     data = fetch_data("SELECT * FROM weather")
    #     st.dataframe(data)

    # elif operation == "Update":
    #     current_weather = st.selectbox("Set Current Weather Condition", ["Optimal", "Rainy", "Snowy"])
    #     if st.button("Update Weather Condition"):
    #         query = "UPDATE weather SET Current_Weather = %s"
    #         execute_query(query, (current_weather,))
    #         st.success(f"Weather condition updated to {current_weather}!")

