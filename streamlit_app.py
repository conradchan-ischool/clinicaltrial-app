import streamlit as st

def find_trials(patient):
    """Function to find clinical trials."""
    st.write("Searching for clinical trials for", patient["condition"]," ...")
    
def main():
    st.title("Clinical Trials App")
    st.write(
        "Find a clinical trial that's right for you."
    )
    st.write(
        "Enter your information below."
    )

    patient_form = st.form(key="patient")
    condition = patient_form.text_input("Medical Condition")
    age = patient_form.number_input("Age", 0, 100, 0, 1)

    # sex = st.radio("Sex", ["Male", "Female"])
    sex = patient_form.radio("Sex", ["Male", "Female", "Both"])
    allowsHealthy = patient_form.checkbox("Allows healthy people", value=False)

    location = patient_form.text_input("Location")
    distance = patient_form.number_input("Miles you are able to travel")

    submit_button = patient_form.form_submit_button(label="Find clinical trials")
    if submit_button:
        # Create a dictionary for the patient profile
        patient = {}
        patient["condition"] = condition
        patient["age"] = age
        patient["sex"] = sex
        patient["allowsHealthy"] = allowsHealthy
        patient["location"] = location
        patient["distance"] = distance
        
        find_trials(patient)
        
        
    
if __name__ == "__main__":
    main()
    

