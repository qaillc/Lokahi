import streamlit as st
import csv
import io
import random
from datetime import datetime, timedelta

st.title("Wearable Data Generator")

# User inputs
num_patients = st.number_input("Number of Patients", min_value=1, value=40)
num_measurements = st.number_input("Measurements per Patient", min_value=1, value=10)
start_date = st.date_input("Start Date", value=datetime(2024, 12, 1))
start_time = st.time_input("Start Time", value=datetime(2024, 12, 1, 8, 0).time())

st.write("This tool generates mock wearable data for patients, some of whom have cancer and may exhibit signs of chemo brain.")

# Additional parameters
cancer_rate = st.slider("Percentage of Patients with Cancer", 0, 100, 30)  # 30% by default
chemo_brain_effect = st.slider("Chemo Brain Impact on Activity Level (in % reduction)", 0, 50, 20)

# Generate data when user clicks
if st.button("Generate Data"):
    # Convert start_date and start_time into a datetime
    start_datetime = datetime.combine(start_date, start_time)

    # Time interval: 1 hour increments
    time_interval = timedelta(hours=1)
    
    # Generate unique PRIMARY_PERSON_KEYs
    # We'll create a pattern of keys - hex-like strings
    base_key = "7D2E50BB328E34917766B7A"
    patient_keys = [base_key + format(i, 'X') for i in range(1, num_patients + 1)]

    # Determine which patients have cancer
    # Randomly assign cancer to the given percentage of patients
    num_cancer_patients = int((cancer_rate / 100) * num_patients)
    cancer_patients = set(random.sample(patient_keys, num_cancer_patients))

    # Generate data
    # Baseline measurements
    baseline_activity = 2000
    baseline_heart_rate = 80
    baseline_o2 = 98.2

    # For chemo brain patients, reduce activity by a percentage
    # e.g., chemo brain patient might have a 20% reduction in activity
    # also maybe increase heart rate slightly
    activity_reduction_factor = (100 - chemo_brain_effect) / 100.0
    chemo_heart_rate_increase = 5  # Increase HR by 5 bpm to simulate stress

    data_rows = []
    
    # Prepare timestamps
    timestamps = [start_datetime + i * time_interval for i in range(num_measurements)]

    # Generate random variability
    for pkey in patient_keys:
        is_cancer = pkey in cancer_patients
        for ts in timestamps:
            # Introduce some random variability
            activity_var = random.randint(-300, 300)
            hr_var = random.randint(-3, 3)
            o2_var = random.uniform(-0.3, 0.3)

            if is_cancer:
                # Apply chemo brain effects
                activity = int((baseline_activity + activity_var) * activity_reduction_factor)
                heart_rate = baseline_heart_rate + hr_var + chemo_heart_rate_increase
            else:
                activity = baseline_activity + activity_var
                heart_rate = baseline_heart_rate + hr_var

            o2_sat = baseline_o2 + o2_var

            # Ensure no negative values
            if activity < 0:
                activity = 0
            if heart_rate < 50:
                heart_rate = 50
            if o2_sat < 90:
                o2_sat = 90.0

            data_rows.append([
                pkey,
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                activity,
                heart_rate,
                round(o2_sat, 1)
            ])

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["PRIMARY_PERSON_KEY", "Measurement_Timestamp", "Activity_Level", "Heart_Rate", "O2_Saturation"])
    writer.writerows(data_rows)

    csv_data = output.getvalue().encode('utf-8')

    st.success("Data generated successfully!")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="Wearable_Data.csv",
        mime="text/csv"
    )
