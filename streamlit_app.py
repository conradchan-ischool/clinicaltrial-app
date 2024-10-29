import streamlit as st
from streamlit_searchbox import st_searchbox
import json
# from difflib import get_close_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
    

def load_conditions():
    """
    Load list of medical conditions from a file into global variable CONDITIONS_LIST.
    File should be in same directory as this file.
    """
    global CONDITIONS_LIST
    CONDITIONS_LIST = []
    
    conditions_filename = "conditions.txt"
    
    with open(conditions_filename, 'r') as conditions_file:
        for line in conditions_file:
            CONDITIONS_LIST.append(line.rstrip())  # Strip out whitespace, newlines


def find_conditions(searchTerm: str) -> list[any]:
    """
    Takes a string and returns a list of potential matches.

    Args:
        searchTerm (str): String to match

    Returns:
        List[any]: List of strings that are partial matches, sorted by closeness.
    """
    
    # return get_close_matches(searchTerm, CONDITIONS_LIST)
    return process.extract(searchTerm, CONDITIONS_LIST)
    

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
    for idx, ct in enumerate(json_list):
            
            # Show brief title if available, otherwise show official title
            briefTitle_list = find_in_json(ct, "briefTitle")
            officialTitle_list = find_in_json(ct, "officialTitle")
            if briefTitle_list:
                expander_heading = briefTitle_list[0]
            else:
                expander_heading = officialTitle_list[0]
            
            with st.expander(expander_heading):
                # Show either detailed description of brief summary
                detailedDescription_list = find_in_json(ct, "detailedDescription")
                briefSummary_list = find_in_json(ct, "briefSummary")
                if detailedDescription_list:
                    st.text("Detailed Description:")
                    st.write(detailedDescription_list[0])
                elif briefSummary_list:
                    st.text("Brief Summary:")
                    st.write(briefSummary_list[0])
                    
                # Show eligibility criteria
                eligibilityCriteria_list = find_in_json(ct, "eligibilityCriteria")
                if eligibilityCriteria_list:
                    st.text("Eligibility Criteria:")
                    st.write(eligibilityCriteria_list[0])
                
                # Show link to clinicaltrials.gov
                nctId = find_in_json(ct,"nctId")[0]
                url = f"https://clinicaltrials.gov/study/{nctId}"
                st.markdown("[See more details on ClinicalTrials.gov website](%s)" % url)

    
def main():
    
    load_conditions() # Load list of medical conditions user can search from
    
    st.title("AllTrials.info")
    st.header("Matching Clinical Trials")
    
    # Enter search criteria in the sidebar
    with st.sidebar:
        st.title("Search for Clinical Trials")
        st.write(
                    "Enter your information below."
                )   
        age = st.number_input("Age", 0, 100, 0, 1)
        sex = st.radio("Sex", ["Female", "Male"])
        # condition = st.text_input("Medical Condition")
        condition = st_searchbox(search_function=find_conditions,
                                 label="Medical Condition",
                                 key="condition_searchbox")
        conditionText = st.text_area("Additional Information")
        acceptsHealthy = st.checkbox("Accepts healthy volunteers", value=False)
        location = st.text_input("Location")
        distance = st.number_input("Miles you are able to travel", 0, 10000, 0, 1)

        submit_button = st.button(label="Find clinical trials")
    
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
        st.write("We found ", len(ct_results), "clinical trials you might qualify for.")
        show_clinical_trials(ct_results)
                        
        
    
if __name__ == "__main__":
    main()
    

