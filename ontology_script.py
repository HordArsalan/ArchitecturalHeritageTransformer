from flask import Flask, request, render_template
from collections import Counter
from owlready2 import get_ontology
from rapidfuzz import fuzz  # Importing RapidFuzz for fuzzy matching

app = Flask(__name__)
import sys
print("Python interpreter path:", sys.executable)

# Load the ontology
ontology_path = "/Users/hordarsalan/Documents/PHD/AHT_Ontology.rdf"
onto = get_ontology(ontology_path).load()

# Define standardized term functions
def get_standardized_term(response_text, class_name, threshold=70):
    """
    Matches a response text to standardized terms using RapidFuzz
    and returns the most common matching term.
    """
    try:
        ontology_class = getattr(onto, class_name, None)
        if ontology_class is None:
            print(f"Class {class_name} not found in ontology.")
            return "Unknown"

        instances = list(ontology_class.instances())
        print(f"Processing response: '{response_text}' against {len(instances)} instances in {class_name}")
        matching_terms = []

        for instance in instances:
            if instance.comment:
                for c in instance.comment:
                    # Convert the comment to string if it's not already
                    c = str(c) if not isinstance(c, str) else c
                    similarity = fuzz.partial_ratio(response_text.lower(), c.lower())
                    print(f"Comparing '{response_text}' with '{c}' (similarity: {similarity})")
                    if similarity >= threshold:
                        if hasattr(instance, 'standardizedAs') and instance.standardizedAs:
                            standardized_instance = instance.standardizedAs[0]
                            if standardized_instance.comment:
                                matching_terms.append(standardized_instance.comment[0])
                                print(f"Matched term: {standardized_instance.comment[0]}")

        if matching_terms:
            most_common = Counter(matching_terms).most_common(1)[0][0]
            print(f"Most common matching term: {most_common}")
            return most_common
        else:
            print("No matching terms found.")
    except AttributeError as e:
        print(f"Error processing term: {e}")
    return "Unknown"

def get_all_architectural_elements(responses, class_name, threshold=70):
    """
    Process architectural elements (HQ2_1):
    - Map plain language responses to standardized terms using fuzzy logic.
    - Count occurrences of each standardized architectural element.
    - Return all distinct elements sorted by frequency.
    """
    standardized_terms = []
    try:
        ontology_class = getattr(onto, class_name, None)
        if ontology_class is None:
            return "Unknown"

        instances = list(ontology_class.instances())
        for response_text in responses:
            for instance in instances:
                if instance.comment:
                    for c in instance.comment:
                        similarity = fuzz.partial_ratio(response_text.lower(), c.lower())
                        if similarity >= threshold:
                            if hasattr(instance, 'standardizedAs') and instance.standardizedAs:
                                standardized_instance = instance.standardizedAs[0]
                                if standardized_instance.comment:
                                    standardized_terms.append(standardized_instance.comment[0])
    except AttributeError:
        pass

    if standardized_terms:
        term_counts = Counter(standardized_terms)  # Count occurrences
        sorted_terms = [term for term, _ in term_counts.most_common()]  # Sort by frequency
        return ", ".join(sorted_terms)  # Return as a comma-separated string
    return "Unknown"

def get_majority_term(responses, class_name, threshold=70):
    """
    Get the term with the highest frequency among responses using fuzzy matching.
    """
    terms = []
    for response in responses:
        term = get_standardized_term(response, class_name, threshold)
        if term:
            terms.append(term)
    if terms:
        return Counter(terms).most_common(1)[0][0]  # Return the most common term
    return "Unknown"

def clean_shept(shept):
    """
    Cleans the SHePT prompt by removing 'Unknown' phrases and fixing dangling text fragments.
    """
    # Define parts to remove
    parts_to_remove = [
        "made of Unknown",
        "designed by Unknown",
        "restoration: Unknown",
        "Signs of deterioration include Unknown",
        "Currently, it is used for Unknown",
        "Plans for the future include Unknown",
        ", Unknown",
        "Unknown, the building was",
        "It underwent Unknown",
        "It underwent"  # Additional cleaning for "It underwent"
    ]

    # Remove unwanted phrases
    for part in parts_to_remove:
        shept = shept.replace(part, "").strip()

    # Remove extra punctuation and spaces
    while "  " in shept:
        shept = shept.replace("  ", " ")  # Clean up multiple spaces
    shept = shept.replace(" ,", ",").replace("..", ".").replace(" .", ".")

    # Ensure the sentence ends cleanly
    shept = shept.strip(", .")  # Remove trailing punctuation
    if shept.endswith("."):
        shept = shept.rstrip(".") + "."

    return shept

# Route to display the form
@app.route('/')
def form():
    return render_template('heritage_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def process_form():
    form_data = request.form
    responses_cq1_1 = form_data.getlist('CQ1_1[]')
    responses_cq1_2 = form_data.getlist('CQ1_2[]')
    responses_cq1_3 = form_data.getlist('CQ1_3[]')
    responses_cq1_4 = form_data.getlist('CQ1_4[]')
    responses_cq2_1 = form_data.getlist('CQ2_1[]')  # Architectural Elements
    responses_cq2_2 = form_data.getlist('CQ2_2[]')
    responses_cq3_1 = form_data.getlist('CQ3_1[]')
    responses_cq3_2 = form_data.getlist('CQ3_2[]')
    responses_cq3_3 = form_data.getlist('CQ3_3[]')
    responses_cq4_1 = form_data.getlist('CQ4_1[]')
    responses_cq4_2 = form_data.getlist('CQ4_2[]')
    responses_cq5_1 = form_data.getlist('CQ5_1[]')
    responses_cq5_2 = form_data.getlist('CQ5_2[]')

    # Use the majority vote function to determine the final terms
    storey_term = get_majority_term(responses_cq1_1, 'CQ1_1')
    building_type_term = get_majority_term(responses_cq1_2, 'CQ1_2')
    style_term = get_majority_term(responses_cq1_3, 'CQ1_3')
    material_term = get_majority_term(responses_cq1_4, 'CQ1_4')
    architectural_elements = get_all_architectural_elements(responses_cq2_1, 'CQ2_1')
    element_materials = get_majority_term(responses_cq2_2, 'CQ2_2')
    architect = get_majority_term(responses_cq3_1, 'CQ3_1')
    restoration_details = get_majority_term(responses_cq3_2, 'CQ3_2')
    deterioration_signs = get_majority_term(responses_cq3_3, 'CQ3_3')
    current_use = get_majority_term(responses_cq4_1, 'CQ4_1')
    future_plans = get_majority_term(responses_cq4_2, 'CQ4_2')
    location = get_majority_term(responses_cq5_1, 'CQ5_1')
    context_environment = get_majority_term(responses_cq5_2, 'CQ5_2')

    # Generate the SHePT prompt
    shept_prompt = (
        f"Generate a front view facade of a {storey_term} {building_type_term}, styled in the {style_term}. "
        f"The building is constructed of {material_term}. Architectural elements include {architectural_elements} made of {element_materials}. "
        f"Situated in {location} {context_environment}, the building was designed by {architect}. "
        f"It underwent restoration: {restoration_details}. Signs of deterioration include {deterioration_signs}. "
        f"Currently, it is used for {current_use}. Plans for the future include {future_plans}."
    )

    # Clean the SHePT prompt to remove specific "Unknown" parts and "It underwent"
    clean_shept_prompt = clean_shept(shept_prompt).replace("It underwent", "").strip()

    # Render the result on the browser
    return render_template('result.html', shept_prompt=clean_shept_prompt)

# Ensure Flask runs correctly
if __name__ == '__main__':
    app.run(debug=True)
