from erdiagram import ER
import json
import pandas as pd
g = ER()

try:
    with open('data.json','r') as F:
        data = json.load(F)
    print("data loaded successfully")
except FileNotFoundError:
    print("couldnt find file")
except json.JSONDecodeError:
    print("JSON format error")
except Exception as e:
    print(f"error occurred {e}")
entities = {}
for entity_data in data.get('entities' , []):
    entity_name = entity_data['name']
    attributes = []
    for attr in entity_data.get('attributes' , []):
        attribute_name = attr['name']
        is_pk = attr.get('isPrimaryKey' , False)
        is_mv = attr.get('isMultiValue' , False)
        composite_parts = attr.get('composite') if attr.get('composite') else []
        try:
            g.add_attribute(entity_name,attribute_name,is_pk,is_mv,False,composite_parts)
        except e:
            pass
for relation in data.get('relationships' , []):
    entity1_name = relation.get('entity1')
    entity2_name = relation.get('entity2')
    relation_name = relation.get('name')
    relation_cardinality = relation.get('cardinality')
    cardinality_parts = relation_cardinality.split(':')
    # print(f"{entity1_name} , {entity2_name} , {relation_name} , {cardinality_parts}")
    g.add_relation({entity1_name : cardinality_parts[0]},relation_name,{entity2_name : cardinality_parts[1]})

diagram = g.draw()
diagram.render("diagram", format="png", view=False, cleanup=True, engine="dot")