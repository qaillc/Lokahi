import streamlit as st


# Display an image
st.image("patienttalk.png", caption="Patient Talk")


# Display the clickable link
st.markdown(
    '[Click here to visit the app](https://chatgpt.com/g/g-cBp7DBgok-patient-talk)', 
    unsafe_allow_html=True
)
