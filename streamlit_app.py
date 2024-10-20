import streamlit as st
import json

def find_in_json(data, key):
    """
    Recursively find value for key in a json structure.
    Args:
        data (json): json to be searched
        key (string): key to be searched for
    Output:
        List of the values for the key
    """
    
    values = []
     
    if isinstance(data, dict): 
        for k, v in data.items(): 
            if k == key: 
                values.append(v) 
            values.extend(find_in_json(v, key)) 
    elif isinstance(data, list): 
        for item in data: 
            values.extend(find_in_json(item, key)) 
     
    return values
    
def call_retrieve_trials_API(patient):
    """
    Call the API to get matching clinical trials.
    For now, this will read a json file of clinical trials.
    """
    clinical_trials_file = open("clinical_trials_sample.json")

    return json.load(clinical_trials_file)


def find_trials(patient):
    """
    Function to find clinical trials.
    Args:
        patient (dict): patient information
    Output:
        list of jsons for clinical trials
    """
    
    return call_retrieve_trials_API(patient)

def show_clinical_trials(json_list):
    """
    Show clinical trials

    Args:
        json_list (list of jsons): List of clinical trials as jsons
    Output:
        None
    """
    for idx, ct in enumerate(ct_results):
            
            # Show brief title if available, otherwise show official title
            briefTitle_list = find_in_json(ct, "briefTitle")
            officialTitle_list = find_in_json(ct, "officialTitle")
            if briefTitle_list:
                expander_heading = briefTitle_list[0]
            else:
                expander_heading = officialTitle_list[0]
            
            with st.expander(expander_heading):
                detailedDescription_list = find_in_json(ct, "detailedDescription")
                if detailedDescription_list:
                    st.text("Detailed Description:")
                    st.write(find_in_json(ct, "detailedDescription")[0])
                
                nctId = find_in_json(ct,"nctId")[0]
                url = f"https://clinicaltrials.gov/study/{nctId}"
                st.markdown("[View in ClinicalTrials.gov website](%s)" % url)

    
def main():
    
    st.title("AllTrials.ai")
    st.header("Matching Clinical Trials")
    
    st.sidebar.title("Search for Clinical Trials")
    st.sidebar.write(
        "Enter your information below."
    )

    # patient_form = st.form(key="patient")
    
    age = st.sidebar.number_input("Age", 0, 100, 0, 1)
    sex = st.sidebar.radio("Sex", ["Female", "Male"])
    condition = st.sidebar.text_input("Medical Condition")
    conditionText = st.sidebar.text_area("Additional Information")
    acceptsHealthy = st.sidebar.checkbox("Accepts healthy volunteers", value=False)
    location = st.sidebar.text_input("Location")
    distance = st.sidebar.number_input("Miles you are able to travel", 0, 10000, 0, 1)

    submit_button = st.sidebar.button(label="Find clinical trials")
    if submit_button:
        # Create a dictionary for the patient profile
        patient = {}
        patient["condition"] = condition
        patient["conditionText"] = conditionText
        patient["age"] = age
        patient["sex"] = sex
        patient["acceptsHealthy"] = acceptsHealthy
        patient["location"] = location
        patient["distance"] = distance
        
        ct_results = find_trials(patient)
        
        # Display results
        st.write(len(ct_results), "clinical trials found.")
        show_clinical_trials(ct_results)
                        
        
    
if __name__ == "__main__":
    main()
    

