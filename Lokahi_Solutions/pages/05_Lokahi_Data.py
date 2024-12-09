import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)

# Function to generate synthetic BreastCancer data
def generate_breast_cancer_data(num_patients):
    primary_keys = [f"PPK_{i+1:05d}" for i in range(num_patients)]
    ages = []
    menopausal_status = []
    tumor_sizes = []
    lymph_nodes = []
    grades = []
    stages = []
    er_status = []
    pr_status = []
    her2_status = []
    ki67_level = []
    tnbc_status = []
    brca_mutation = []
    overall_health = []
    genomic_score = []
    treatment = []

    for i in range(num_patients):
        age = int(np.random.normal(60, 10))
        age = max(30, min(age, 80))
        ages.append(age)

        menopausal = "Post-menopausal" if age >= 50 else "Pre-menopausal"
        menopausal_status.append(menopausal)

        tumor_size = round(np.random.lognormal(mean=0.7, sigma=0.5), 2)
        tumor_sizes.append(tumor_size)

        lymph_node = (
            "Positive"
            if (tumor_size > 2.0 and np.random.rand() < 0.6)
            or (tumor_size <= 2.0 and np.random.rand() < 0.3)
            else "Negative"
        )
        lymph_nodes.append(lymph_node)

        grade = np.random.choice([1, 2, 3], p=[0.1, 0.4, 0.5] if tumor_size > 2.0 else [0.3, 0.5, 0.2])
        grades.append(grade)

        if tumor_size <= 2.0 and lymph_node == "Negative":
            stage = "I"
        elif (tumor_size > 2.0 and tumor_size <= 5.0) and lymph_node == "Negative":
            stage = "II"
        elif lymph_node == "Positive" or tumor_size > 5.0:
            stage = "III"
        else:
            stage = "II"
        if np.random.rand() < 0.05:
            stage = "IV"
        stages.append(stage)

        er = np.random.choice(["Positive", "Negative"], p=[0.75, 0.25])
        pr = "Positive" if er == "Positive" and np.random.rand() > 0.1 else "Negative"
        er_status.append(er)
        pr_status.append(pr)

        her2 = np.random.choice(["Positive", "Negative"], p=[0.3, 0.7] if grade == 3 else [0.15, 0.85])
        her2_status.append(her2)

        ki67 = "High" if grade == 3 and np.random.rand() < 0.8 else "Low"
        ki67_level.append(ki67)

        tnbc = "Positive" if er == "Negative" and pr == "Negative" and her2 == "Negative" else "Negative"
        tnbc_status.append(tnbc)

        brca = "Positive" if (tnbc == "Positive" or age < 40) and np.random.rand() < 0.2 else "Negative"
        brca_mutation.append(brca)

        health = "Good" if age < 65 and np.random.rand() < 0.9 else "Poor"
        overall_health.append(health)

        recurrence_score = (
            np.random.choice(["Low", "Intermediate", "High"], p=[0.6, 0.3, 0.1])
            if er == "Positive" and her2 == "Negative"
            else "N/A"
        )
        genomic_score.append(recurrence_score)

        if stage in ["I", "II"]:
            if tnbc == "Positive":
                treat = "Surgery, Chemotherapy, and Radiation Therapy"
            elif er == "Positive" and recurrence_score != "N/A":
                if recurrence_score == "High":
                    treat = "Surgery, Chemotherapy, Hormone Therapy, and Radiation Therapy"
                elif recurrence_score == "Intermediate":
                    treat = "Surgery, Consider Chemotherapy, Hormone Therapy, and Radiation Therapy"
                else:
                    treat = "Surgery, Hormone Therapy, and Radiation Therapy"
            elif her2 == "Positive":
                treat = "Surgery, HER2-Targeted Therapy, Chemotherapy, and Radiation Therapy"
            else:
                treat = "Surgery, Chemotherapy, and Radiation Therapy"
        elif stage == "III":
            treat = (
                "Neoadjuvant Chemotherapy, Surgery, Radiation Therapy"
                + (", HER2-Targeted Therapy" if her2 == "Positive" else "")
                + (", Hormone Therapy" if er == "Positive" else "")
            )
        else:
            treat = "Systemic Therapy (Palliative Care)"
        treatment.append(treat)

    breast_cancer_data = {
        "PRIMARY_PERSON_KEY": primary_keys,
        "Age": ages,
        "Menopausal Status": menopausal_status,
        "Tumor Size (cm)": tumor_sizes,
        "Lymph Node Involvement": lymph_nodes,
        "Tumor Grade": grades,
        "Tumor Stage": stages,
        "ER Status": er_status,
        "PR Status": pr_status,
        "HER2 Status": her2_status,
        "Ki-67 Level": ki67_level,
        "TNBC Status": tnbc_status,
        "BRCA Mutation": brca_mutation,
        "Overall Health": overall_health,
        "Genomic Recurrence Score": genomic_score,
        "Treatment": treatment,
    }

    return pd.DataFrame(breast_cancer_data)

# Function to generate Members
def generate_members_from_breast_cancer(breast_cancer_df):
    return pd.DataFrame({
        "MEMBER_ID": breast_cancer_df["PRIMARY_PERSON_KEY"],
        "PRIMARY_PERSON_KEY": breast_cancer_df["PRIMARY_PERSON_KEY"],
        "MEM_GENDER": ["F"] * len(breast_cancer_df),
        "MEM_ETHNICITY": np.random.choice(["Hispanic", "Non-Hispanic", None], len(breast_cancer_df)),
        "MEM_RACE": np.random.choice(["White", "Black", "Asian", None], len(breast_cancer_df)),
        "MEM_STATE": np.random.choice(["MI", "HI", "CA"], len(breast_cancer_df)),
        "MEM_ZIP3": np.random.randint(100, 999, len(breast_cancer_df)),
    })

# Function to generate Enrollments
def generate_enrollments_from_breast_cancer(breast_cancer_df):
    return pd.DataFrame({
        "PRIMARY_PERSON_KEY": breast_cancer_df["PRIMARY_PERSON_KEY"],
        "MEM_STAT": np.random.choice(["ACTIVE", "INACTIVE"], len(breast_cancer_df)),
        "PAYER_LOB": np.random.choice(["MEDICAID", "COMMERCIAL", "MEDICARE"], len(breast_cancer_df)),
        "PAYER_TYPE": np.random.choice(["PPO", "HMO"], len(breast_cancer_df)),
        "RELATION": np.random.choice(["SUBSCRIBER", "DEPENDENT"], len(breast_cancer_df)),
    })

# Function to generate Services
def generate_services(num_services, primary_keys):
    return pd.DataFrame({
        "PRIMARY_PERSON_KEY": np.random.choice(primary_keys, num_services),
        "SERVICE_SETTING": np.random.choice(["OUTPATIENT", "INPATIENT"], num_services),
        "PROC_CODE": np.random.randint(1000, 9999, num_services),
        "SERVICE_DATE": pd.date_range(start="2023-01-01", periods=num_services).to_numpy(),
        "AMOUNT_BILLED": np.random.uniform(500, 15000, num_services),
        "AMOUNT_PAID": np.random.uniform(500, 15000, num_services),
        "CLAIM_STATUS": np.random.choice(["PAID", "DENIED", "PENDING"], num_services),
        "RELATION": np.random.choice(["SUBSCRIBER", "DEPENDENT"], num_services),
    })

# Function to generate Providers
def generate_providers(num_providers):
    return pd.DataFrame({
        "PROVIDER_ID": [f"PROV_{i+1:05d}" for i in range(num_providers)],
        "PROV_NAME": np.random.choice(["Clinic A", "Clinic B", "Clinic C"], num_providers),
        "PROV_STATE": np.random.choice(["MI", "HI", "CA"], num_providers),
        "PROV_ZIP": np.random.randint(10000, 99999, num_providers),
        "PROV_SPECIALTY": np.random.choice(["Oncology", "Radiology", "Surgery"], num_providers),
        "PROV_TAXONOMY": np.random.choice(["208100000X", "207RE0101X"], num_providers),
    })

# Function to generate Wearable Data
def generate_wearable_data(num_patients, num_measurements, start_datetime, time_interval, cancer_rate, chemo_brain_effect, primary_keys):
    num_cancer_patients = int((cancer_rate / 100) * num_patients)
    cancer_patients = set(random.sample(primary_keys, num_cancer_patients))
    baseline_activity = 2000
    baseline_heart_rate = 80
    baseline_o2 = 98.2
    activity_reduction_factor = (100 - chemo_brain_effect) / 100.0
    chemo_heart_rate_increase = 5

    data_rows = []
    timestamps = [start_datetime + i * time_interval for i in range(num_measurements)]

    for pkey in primary_keys:
        is_cancer = pkey in cancer_patients
        for ts in timestamps:
            activity_var = random.randint(-300, 300)
            hr_var = random.randint(-3, 3)
            o2_var = random.uniform(-0.3, 0.3)

            if is_cancer:
                activity = int((baseline_activity + activity_var) * activity_reduction_factor)
                heart_rate = baseline_heart_rate + hr_var + chemo_heart_rate_increase
            else:
                activity = baseline_activity + activity_var
                heart_rate = baseline_heart_rate + hr_var

            o2_sat = baseline_o2 + o2_var

            activity = max(activity, 0)
            heart_rate = max(heart_rate, 50)
            o2_sat = max(o2_sat, 90.0)

            data_rows.append([
                pkey,
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                activity,
                heart_rate,
                round(o2_sat, 1)
            ])
    
    return pd.DataFrame(data_rows, columns=["PRIMARY_PERSON_KEY", "Measurement_Timestamp", "Activity_Level", "Heart_Rate", "O2_Saturation"])

# Main Streamlit App
st.title("Lokahi Synthetic Medical Data Generator ")

# Sliders
num_patients = st.slider("Number of Breast Cancer Patients to Generate", 10, 1000, 100)
num_measurements = st.slider("Measurements per Patient (Wearable Data)", 1, 100, 10)
num_services = st.slider("Number of Services to Generate", 10, 2000, 500)
num_providers = st.slider("Number of Providers to Generate", 10, 500, 100)

start_date = st.date_input("Wearable Data Start Date", value=datetime(2024, 12, 1))
start_time = st.time_input("Wearable Data Start Time", value=datetime(2024, 12, 1, 8, 0).time())
cancer_rate = st.slider("Percentage of Patients with Cancer (Wearable Data)", 0, 100, 30)
chemo_brain_effect = st.slider("Chemo Brain Impact on Activity Level (in % reduction)", 0, 50, 20)

if st.button("Generate Data"):
    primary_keys = [f"PPK_{i+1:05d}" for i in range(num_patients)]
    wearable_start_datetime = datetime.combine(start_date, start_time)
    breast_cancer_df = generate_breast_cancer_data(num_patients)
    members_df = generate_members_from_breast_cancer(breast_cancer_df)
    enrollments_df = generate_enrollments_from_breast_cancer(breast_cancer_df)
    services_df = generate_services(num_services, primary_keys)
    providers_df = generate_providers(num_providers)
    wearable_data = generate_wearable_data(
        num_patients, num_measurements, wearable_start_datetime, timedelta(hours=1), cancer_rate, chemo_brain_effect, primary_keys
    )

    st.subheader("Breast Cancer Data")
    st.dataframe(breast_cancer_df.head())
    st.download_button("Download Breast Cancer Data", breast_cancer_df.to_csv(index=False), "breast_cancer.csv")

    st.subheader("Members Data")
    st.dataframe(members_df.head())
    st.download_button("Download Members Data", members_df.to_csv(index=False), "members.csv")

    st.subheader("Enrollments Data")
    st.dataframe(enrollments_df.head())
    st.download_button("Download Enrollments Data", enrollments_df.to_csv(index=False), "enrollments.csv")

    st.subheader("Services Data")
    st.dataframe(services_df.head())
    st.download_button("Download Services Data", services_df.to_csv(index=False), "services.csv")

    st.subheader("Providers Data")
    st.dataframe(providers_df.head())
    st.download_button("Download Providers Data", providers_df.to_csv(index=False), "providers.csv")

    st.subheader("Wearable Data")
    st.dataframe(wearable_data.head())
    st.download_button("Download Wearable Data", wearable_data.to_csv(index=False), "wearable_data.csv")

