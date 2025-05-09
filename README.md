Echo-based Heritage Digital Twin (EH-DT) Toolkit
Overview
The Echo-based Heritage Digital Twin (EH-DT) Toolkit is an AI-integrated toolset designed to reconstruct lost or partially lost architectural heritage using intangible data like oral histories. The tool moves beyond traditional Heritage Building Information Modelling (HBIM) by generating Standardised Heritage Prompts (SHePT) that can be used in AI text-to-image generation tools to visualise buildings from memory-based descriptions. This work is part of a broader research project on expanding HBIM into AI-enabled Digital Twin workflows.

Key Components
ontology_script.py: Automates the conversion of plain language responses into structured architectural terminology using the AHT ontology.

AHT_Ontology.rdf: The Architectural Heritage Transformer (AHT) ontology in OWL/Turtle format, linking descriptive terms to architectural concepts.

app.py: Flask-based user interface for entering heritage descriptions and generating outputs.

form_templates/: HTML forms used to collect data about lost heritage from experts and non-experts.

requirements.txt: List of required Python packages for running the tool.

generate_prompt.py: (deprecated in latest version) Original script for generating prompts — now integrated into ontology_script.py.

Workflow Summary
Oral Data Collection
Users fill a web form based on 14 Heritage Questions (HQs), reflecting memories of a specific building.

Ontology Mapping
Plain Language Responses (PLRs) are linked to architectural terms using the AHT ontology via automated querying.

Prompt Generation
Standardised architectural descriptions are merged into a SHePT prompt, ready for input into AI image generators such as DALL·E or Midjourney.

AI Visualisation
The generated prompt can be used to create a visual digital twin of a lost heritage building based on collective memory.

Installation
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/HordArsalan/EH-DT-Toolkit.git
cd EH-DT-Toolkit
2. Set up the Python Environment
Install required libraries:

bash
Copy
Edit
pip install -r requirements.txt
3. Run the Application
bash
Copy
Edit
python app.py
Then, open your browser and go to http://127.0.0.1:5000/

Folder Structure
graphql
Copy
Edit
EH-DT-Toolkit/
│
├── AHT_Ontology.rdf             # Ontology file
├── app.py                       # Flask app for user interface
├── ontology_script.py           # Ontology querying & prompt generator
├── generate_prompt.py           # (Legacy) Old script version
├── requirements.txt             # Dependencies
├── form_templates/              # HTML forms for HQs
├── static/                      # Optional: CSS/images
└── README.md                    # You are here!
Citation
If you use this toolkit in your work, please cite:

Arsalan, H., Heesom, D., & Moore, N. (2025). From Heritage Building Information Modelling Towards an ‘Echo-Based’ Heritage Digital Twin. Heritage, 8(1), 33. https://doi.org/10.3390/heritage8010033