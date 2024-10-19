import streamlit as st
import json

def call_retrieve_trials_API(patient):
    """
    Call the API to get matching clinical trials.
    For now, this will read a json file of clinical trials.
    """
    clinical_trials_file = open("clinical_trials_sample.json")

    return json.load(clinical_trials_file)


def find_trials(patient):
    """Function to find clinical trials."""
    st.write("Searching for clinical trials for", patient["condition"]," ...")
    return call_retrieve_trials_API(patient)
    
    
def main():
    st.title("Clinical Trials App")
    st.sidebar.write(
        "Find a clinical trial that's right for you."
    )
    st.sidebar.write(
        "Enter your information below."
    )

    # patient_form = st.form(key="patient")
    
    age = st.sidebar.number_input("Age", 0, 100, 0, 1)
    sex = st.sidebar.radio("Sex", ["Female", "Male"])
    condition = st.sidebar.text_input("Medical Condition")
    acceptsHealthy = st.sidebar.checkbox("Accepts healthy volunteers", value=False)
    location = st.sidebar.text_input("Location")
    distance = st.sidebar.number_input("Miles you are able to travel", 0, 10000, 0, 1)

    submit_button = st.sidebar.button(label="Find clinical trials")
    if submit_button:
        # Create a dictionary for the patient profile
        patient = {}
        patient["condition"] = condition
        patient["age"] = age
        patient["sex"] = sex
        patient["acceptsHealthy"] = acceptsHealthy
        patient["location"] = location
        patient["distance"] = distance
        
        find_trials(patient)
        
        # Display results
        
        
    
if __name__ == "__main__":
    main()
    

