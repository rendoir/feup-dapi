# Semantic Web and Ontologies

## View Ontology

To view the ontology import the OWL file  
- **GameOntology.owl**: Ontology modelled but without individuals  
- **GameOntologyPopulated.owl**: Ontology populated with data from the dataset

## Populate the ontology
1. Import **GameOntology.owl**
2. [Optional] Generate CSV files from **dataset.jl**  
    2.1. Run
    ```bash
    python3 json_to_csv.py
    ```
    2.2. Add each CSV to a spreadsheet, one per tab  
3. Inside Protégé, go to 'Tools -> Create axioms from Excel workbook' and select the spreadsheet
4. Click 'Load Rules' and select the **rules.json** file
5. Click 'Generate axioms'

## Query the ontology
The **queries** folder contains all the queries in SPARQL.  
In Protégé, open the **SPARQL Query** tab.  
To run a query simply copy it, including the prefixes, paste it inside the tab and click 'Execute'.
