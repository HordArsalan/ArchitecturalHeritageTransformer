from owlready2 import *

# Load the ontology
onto_path.append("/Users/hordarsalan/Documents/MyOntoScripts")  # Replace with the path to your ontology file
ontology = get_ontology("file:///Users/hordarsalan/Documents/MyOntoScripts/AHT.rdf").load()

# Define the function to generate the template
def generate_prompt_template(building_instance):
    template = {
        "Name of Building": building_instance.name,
        "Number of Storeys": building_instance.hasNumberOfStoreys,
        "Type of Building": building_instance.hasBuildingType,
        "Style of the Building": building_instance.hasStyle,
        "Age of the Building": building_instance.hasConstructionYear,
        "Construction Material": ", ".join(building_instance.hasConstructionMaterial),
        "Material Colour": building_instance.hasMaterialColor if hasattr(building_instance, 'hasMaterialColor') else "Not specified",
        "Specific Architectural Elements": [elem.name for elem in building_instance.hasArchitecturalElement],
        "Material of Elements": [(elem.name, elem.hasElementMaterialType, elem.hasElementMaterialColor) for elem in building_instance.hasArchitecturalElement],
        "Location/Environment": building_instance.locatedIn if hasattr(building_instance, 'locatedIn') else "Not specified",
        "Architect": building_instance.designedBy if hasattr(building_instance, 'designedBy') else "Not specified",
        "Restoration Details": [(rest.restorationYear, rest.restorationArchitect) for rest in building_instance.underwentRestoration],
        "Signs of Deterioration": [deter.description for deter in building_instance.showsSignsOf],
        "Current Use/Occupancy": building_instance.hasCurrentUse if hasattr(building_instance, 'hasCurrentUse') else "Not specified",
        "Future Plans": building_instance.hasFuturePlan if hasattr(building_instance, 'hasFuturePlan') else "Not specified",
    }
    return template

# Example query for a specific building instance
building_instance = ontology.search_one(label="Church_of_St_Michael_Alberbury_with_Cardeston")  # Replace with the specific building instance label

# Generate the prompt template
if building_instance:
    prompt_template = generate_prompt_template(building_instance)
    for key, value in prompt_template.items():
        print(f"{key}: {value}")
else:
    print("Building instance not found in the ontology.")
