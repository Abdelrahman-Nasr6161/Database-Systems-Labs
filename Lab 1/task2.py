import os 
from google import genai
import argparse
client = genai.Client(api_key = "API_KEY")
prompt = """
    Act as a seasoned **Database Engineer**. You are given a problem statement describing a database system's requirements.

Your task is to analyze the requirements and immediately output a **single JSON object** that models the entities, attributes, and relationships necessary to represent the system.

**[INSTRUCTION]:** Output ONLY the JSON code block. Do not include any text, conversation, greetings, introductory sentences (e.g., "Here is the JSON..."), or trailing symbols (e.g., backticks ```) outside of the JSON structure itself.

Follow this JSON structure precisely:

* **entities:** A list of objects, each with a "name" and an "attributes" list.
* **attributes:** Each attribute must be an object with at least a "name".
    * Identify a **Primary Key** using `"isPrimaryKey": true`.
    * Identify **Composite Attributes** using `"composite": [...]` listing the sub-attributes (e.g. { "name": "Name", "composite": ["FirstName", "LastName"] },).
    do not add attributes within the composite attributes again only once within their composite attribute
    * Identify **Multi-Valued Attributes** using `"isMultiValued": true`.
* **relationships:** A list of objects detailing the "entity1", "entity2", "name" (relationship label), and "cardinality" (e.g., "1:1", "1:N", "N:1", "M:N") also feel free to add specific numbers like "2:1" or "3:N" if the relationship needs that.

**Problem Statement:** We are making a database for the F1 racing series 
the database should contain teams who will have names and ids , 
the ids will be the primary key , 
drivers who will also have name that consists of both first name and last name 
they will also have ids
we need a race entity as well that will have an id , name , location and date
every team may only have 2 and only 2 drivers and every driver is only assigned to one single team
also we need a car entity , each car has an id and model name which both can be classified as primary keys 
each team has 1 and only 1 car
Expected Model Output (Example)

The model, given this modified prompt, should respond with the following, and nothing else:

"""
parser = argparse.ArgumentParser()
parser.add_argument(
    '--interactive',
    action="store_true"
)
args = parser.parse_args()
if args.interactive:
    print("📝 Interactive mode: Please type your prompt below (press ENTER when done):")
    problem_statement = input()
    
try:
    print('Sending your prompt to the client....')
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    print("--- Model Response ---")
    print(response.text)
    print("----------------------")
    with open('data.json','w') as F:
        lines = response.text.splitlines()
        lines = lines[1:-1]
        cleaned_text = "\n".join(lines)
        F.write(cleaned_text)
except Exception as e:
    print(f"An error occurred: {e}") 
