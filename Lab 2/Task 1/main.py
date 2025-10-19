from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import json
from eralchemy import render_er


with open('data.json') as f:
    schema = json.load(f)

Base = declarative_base()
classes = {}

type_map = {
    "String": String,
    "Integer": Integer
}

for ent in schema["entities"]:
    name = ent["name"]
    table_name = name.lower()
    attrs = {"__tablename__": table_name}

    if ent.get("isWeak", False):
        weak_pk_name = f"{table_name}_id"
        attrs[weak_pk_name] = Column(Integer, primary_key=True, autoincrement=True)

    for attr in ent.get("attributes", []):
        col_name = attr["name"]

        if "composite" in attr:
            for comp_field in attr["composite"]:
                attrs[comp_field] = Column(String)
            continue

        if attr.get("isMultiValued"):
            continue

        col_type = String
        if attr.get("type") in type_map:
            col_type = type_map[attr["type"]]

        try:
            if attr.get("isPrimaryKey"):
                attrs[col_name] = Column(col_type, primary_key=True)
            elif attr.get("isPartialKey"):
                attrs[col_name] = Column(col_type, primary_key=True)
            else:
                attrs[col_name] = Column(col_type)
        except Exception:
            pass

    try:
        klass = type(name, (Base,), attrs)
        classes[name] = klass
    except Exception as e:
        print(f"❌ Error creating class {name}: {e}")


for ent in schema["entities"]:
    ent_name = ent["name"]
    base_cls = classes[ent_name]

    pk_attr = next((a for a in ent["attributes"] if a.get("isPrimaryKey")), None)
    if not pk_attr:
        continue
    pk_name = pk_attr["name"]
    pk_type = String

    for attr in ent["attributes"]:
        if not attr.get("isMultiValued"):
            continue

        try:
            attr_name = attr["name"]
            mv_cls_name = f"{ent_name}{attr_name.capitalize()}"
            mv_table_name = f"{ent_name.lower()}_{attr_name.lower()}"

            mv_attrs = {"__tablename__": mv_table_name}

            fk_colname = f"{ent_name.lower()}_{pk_name}"
            mv_attrs[fk_colname] = Column(pk_type, ForeignKey(f"{ent_name.lower()}.{pk_name}"), primary_key=True)

            mv_attrs[attr_name] = Column(String, primary_key=True)

            mv_cls = type(mv_cls_name, (Base,), mv_attrs)
            classes[mv_cls_name] = mv_cls
        except Exception as e:
            print(f"❌ Error creating multivalued class {mv_cls_name}: {e}")


for rel in schema.get("relationships", []):
    rel_name = rel["name"]
    entities = rel["entities"]
    is_identifying = rel.get("isIdentifying", False)

    left_ent = entities[0]["name"]
    right_ent = entities[1]["name"]
    left_card = entities[0]["cardinality"]
    right_card = entities[1]["cardinality"]

    if left_card == "N" and right_card == "1":
        many_side = left_ent
        one_side = right_ent
    elif left_card == "1" and right_card == "N":
        many_side = right_ent
        one_side = left_ent
    else:
        if left_card == "N" and right_card == "N":
            assoc_table_name = f"{left_ent.lower()}_{right_ent.lower()}_{rel_name.lower()}"
            assoc_attrs = {"__tablename__": assoc_table_name}

            left_cls = classes[left_ent]
            left_pk_col = next(col for col in left_cls.__table__.columns if col.primary_key)
            assoc_attrs[f"{left_ent.lower()}_{left_pk_col.name}"] = Column(
                left_pk_col.type.__class__,
                ForeignKey(f"{left_ent.lower()}.{left_pk_col.name}"),
                primary_key=True
            )

            right_cls = classes[right_ent]
            right_pk_col = next(col for col in right_cls.__table__.columns if col.primary_key)
            assoc_attrs[f"{right_ent.lower()}_{right_pk_col.name}"] = Column(
                right_pk_col.type.__class__,
                ForeignKey(f"{right_ent.lower()}.{right_pk_col.name}"),
                primary_key=True
            )

            for attr in rel.get("attributes", []):
                assoc_attrs[attr["name"]] = Column(String)

            assoc_cls = type(f"{left_ent}{right_ent}{rel_name}", (Base,), assoc_attrs)
            classes[f"{left_ent}{right_ent}{rel_name}"] = assoc_cls

            setattr(classes[left_ent], f"{right_ent.lower()}_{rel_name.lower()}s",
                    relationship(classes[right_ent], secondary=assoc_cls.__table__, back_populates=f"{left_ent.lower()}_{rel_name.lower()}s"))
            setattr(classes[right_ent], f"{left_ent.lower()}_{rel_name.lower()}s",
                    relationship(classes[left_ent], secondary=assoc_cls.__table__, back_populates=f"{right_ent.lower()}_{rel_name.lower()}s"))
            continue
        elif left_card == "1" and right_card == "1":
            left_cls = classes[left_ent]
            right_cls = classes[right_ent]

            left_pk_col = next(col for col in left_cls.__table__.columns if col.primary_key)
            fk_name = f"{right_ent.lower()}_{left_pk_col.name}"

            fk_col = Column(
                left_pk_col.type.__class__,
                ForeignKey(f"{left_ent.lower()}.{left_pk_col.name}"),
                unique=True
            )
            setattr(right_cls, fk_name, fk_col)

            setattr(left_cls, f"{right_ent.lower()}_{rel_name.lower()}",
                    relationship(right_cls, back_populates=f"{left_ent.lower()}_{rel_name.lower()}", uselist=False))
            setattr(right_cls, f"{left_ent.lower()}_{rel_name.lower()}",
                    relationship(left_cls, back_populates=f"{right_ent.lower()}_{rel_name.lower()}", uselist=False))

    many_cls = classes[many_side]
    one_cls = classes[one_side]

    one_pk_col = None
    one_pk_type = None
    for col in one_cls.__table__.columns:
        if col.primary_key:
            one_pk_col = col.name
            one_pk_type = col.type.__class__
            break
    if not one_pk_col:
        continue

    fk_col_name = f"{one_side.lower()}_{one_pk_col}"
    if fk_col_name in many_cls.__table__.columns:
        fk_col_name = f"{fk_col_name}_{rel_name.lower()}"

    if not is_identifying:
        setattr(
            many_cls,
            fk_col_name,
            Column(one_pk_type, ForeignKey(f"{one_side.lower()}.{one_pk_col}"))
        )

    rel_name_many = f"{one_side.lower()}_{rel_name.lower()}"
    rel_name_one = f"{many_side.lower()}_{rel_name.lower()}s"

    setattr(many_cls, rel_name_many, relationship(one_cls, back_populates=rel_name_one))
    setattr(one_cls, rel_name_one, relationship(many_cls, back_populates=rel_name_many))


render_er(Base, 'output.png')
print("✅ ER diagram saved to output.png")
