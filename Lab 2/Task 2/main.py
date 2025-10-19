import json
import re

with open('company.json', 'r') as file:
    db = json.load(file)

def print_table(table):
    if not table:
        print("∅")
        return
    headers = table[0].keys()
    print("\t".join(str(h) for h in headers))
    for row in table:
        print("\t".join(str(row[h]) for h in headers))

def select(table, condition_str):
    def match_condition(row):
        return eval(condition_str, {}, row)
    return [row for row in table if match_condition(row)]

def project(table, attributes):
    attrs = [a.strip() for a in attributes.split(",")]
    return [{attr: row[attr] for attr in attrs if attr in row} for row in table]

def join(table1, table2, on_attr, table1_name="T1", table2_name="T2"):
    result = []
    for row1 in table1:
        for row2 in table2:
            if row1[on_attr] == row2[on_attr]:
                merged = {}

                for key, value in row1.items():
                    merged[f"{table1_name}.{key}"] = value

                for key, value in row2.items():
                    merged[f"{table2_name}.{key}"] = value

                result.append(merged)
    return result

def union(table1, table2):
    seen = set()
    result = []
    for row in table1 + table2:
        tup = tuple(sorted(row.items()))
        if tup not in seen:
            seen.add(tup)
            result.append(row)
    return result

def intersect(table1, table2):
    set2 = {tuple(sorted(r.items())) for r in table2}
    return [r for r in table1 if tuple(sorted(r.items())) in set2]

def difference(table1, table2):
    set2 = {tuple(sorted(r.items())) for r in table2}
    return [r for r in table1 if tuple(sorted(r.items())) not in set2]

def aggregate(table, func, attr):
    values = [row[attr] for row in table if attr in row]
    if func == "SUM":
        return [{"SUM("+attr+")": sum(values)}]
    elif func == "AVG":
        return [{"AVG("+attr+")": sum(values) / len(values) if values else 0}]
    elif func == "MIN":
        return [{"MIN("+attr+")": min(values)}]
    elif func == "MAX":
        return [{"MAX("+attr+")": max(values)}]
    elif func == "COUNT":
        return [{"COUNT("+attr+")": len(values)}]
    else:
        raise ValueError(f"Unknown aggregate function: {func}")

def execute_query(query):
    q = query.strip()
    if q.startswith("SELECT"):
        match = re.match(r"SELECT\s+(\w+)\s+WHERE\s+(.+)", q)
        if match:
            table_name, cond = match.groups()
            return select(db[table_name], cond)
    elif q.startswith("PROJECT"):
        match = re.match(r"PROJECT\s+(.+)\s+FROM\s+(\w+)", q)
        if match:
            attrs, table_name = match.groups()
            return project(db[table_name], attrs)
    elif q.startswith("JOIN"):
        match = re.match(r"JOIN\s+(\w+),(\w+)\s+ON\s+(\w+)", q)
        if match:
            t1, t2, attr = match.groups()
            return join(db[t1], db[t2], attr, t1 ,t2)
    elif q.startswith("UNION"):
        match = re.match(r"UNION\s+(\w+),(\w+)", q )
        if match:
            t1, t2 = match.groups()
            return union(db[t1], db[t2])
    elif q.startswith("INTERSECT"):
        match = re.match(r"INTERSECT\s+(\w+),(\w+)", q)
        if match:
            t1, t2 = match.groups()
            return intersect(db[t1], db[t2])
    elif q.startswith("DIFFERENCE"):
        match = re.match(r"DIFFERENCE\s+(\w+),(\w+)", q)
        if match:
            t1, t2 = match.groups()
            return difference(db[t1], db[t2])
    elif q.startswith("AGGREGATE"):
        match = re.match(r"AGGREGATE\s+(\w+)\((\w+)\)\s+FROM\s+(\w+)", q )
        if match:
            func, attr, table_name = match.groups()
            return aggregate(db[table_name], func.upper(), attr)
    else:
        raise ValueError(f"Unknown or invalid query: {query}")

if __name__ == "__main__":
    while True:
        query = input().strip()
        if query.lower() == "exit":
            break
        try:
            result = execute_query(query)
            print_table(result)
        except Exception as e:
            print("Error:", e)
