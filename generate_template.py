from owlready2 import get_ontology

# Load the ontology
ontology_path = "/Users/hordarsalan/Documents/MyOntoScripts/VictorianHeritage.owx"
onto = get_ontology(ontology_path).load()

# Ensure all individuals are created
def ensure_individual(cls, name):
    individual = onto.search_one(iri=f"*{name}")
    if not individual:
        individual = cls(name)
    return individual

# Ensure all necessary individuals
BayWindows_1 = ensure_individual(onto.BayWindows, "BayWindows_1")
DecorativeCornices_1 = ensure_individual(onto.DecorativeCornices, "DecorativeCornices_1")
SirGeorgeGilbertScott_1 = ensure_individual(onto.Architect, "SirGeorgeGilbertScott_1")
Restoration1995_1 = ensure_individual(onto.Restoration, "Restoration1995_1")
Restoration1996_1 = ensure_individual(onto.Restoration, "Restoration1996_1")
Restoration1997_1 = ensure_individual(onto.Restoration, "Restoration1997_1")
Restoration2007_1 = ensure_individual(onto.Restoration, "Restoration2007_1")
RecentRepairsAndRefurbishment_1 = ensure_individual(onto.Restoration, "RecentRepairsAndRefurbishment_1")
CrumblingFacade_1 = ensure_individual(onto.Deterioration, "CrumblingFacade_1")
Pub_1 = ensure_individual(onto.Use, "Pub_1")
ConversionToOfficeSpace_1 = ensure_individual(onto.Plan, "ConversionToOfficeSpace_1")

# Define the fill_template function
def fill_template(building):
    template = f"A {building.hasNumberOfStoreys[0]}-storey {building.hasType[0]}, styled in the {building.hasArchitecturalStyle[0]}. "
    template += f"The building is constructed of {building.hasConstructionMaterial[0]}. "
    template += f"Architectural elements include {', '.join([element.name for element in building.hasArchitecturalElement])}. "
    template += f"Situated in {building.locatedIn[0]}. The building was designed by {building.designedBy[0].name}. "
    template += f"It underwent restoration {', '.join([restoration.name for restoration in building.underwentRestoration])} and shows signs of {building.showsSignsOf[0].name}. "
    template += f"Currently, it is used for {building.hasCurrentUse[0].name}. Plans for the future include {building.hasFuturePlans[0].name}."
    return template

# Example usage
building = ensure_individual(onto.VictorianHouse, "PrinceAlbert_Wolverhampton")

# Ensure all properties are set correctly
building.hasNumberOfStoreys = [4]
building.hasType = ["Commercial"]
building.hasArchitecturalStyle = ["Victorian"]
building.hasConstructionMaterial = ["Red Brick"]
building.hasArchitecturalElement = [BayWindows_1, DecorativeCornices_1]
building.locatedIn = ["Wolverhampton"]
building.designedBy = [SirGeorgeGilbertScott_1]
building.underwentRestoration = [Restoration1995_1, Restoration1996_1, Restoration1997_1, Restoration2007_1, RecentRepairsAndRefurbishment_1]
building.showsSignsOf = [CrumblingFacade_1]
building.hasCurrentUse = [Pub_1]
building.hasFuturePlans = [ConversionToOfficeSpace_1]

# Print the filled template
print(fill_template(building))
