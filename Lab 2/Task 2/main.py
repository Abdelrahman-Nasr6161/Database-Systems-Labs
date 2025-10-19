import json
import re

try:
    with open('company.json', 'r') as file:
        db = json.load(file)
except FileNotFoundError:
    print("Error: 'company.json' not found. Please ensure the file is in the same directory.")
    exit()


def print_table(table):
    if not isinstance(table, list) or not table:
        print("∅ (Empty set)")
        return
    
    if not all(isinstance(row, dict) for row in table):
        print(table) 
        return

    headers = table[0].keys()
    header_line = "\t".join(str(h) for h in headers)
    print(header_line)
    print("-" * len(header_line.expandtabs())) 

    for row in table:
        print("\t".join(str(row.get(h, 'NULL')) for h in headers))


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
            if on_attr in row1 and on_attr in row2 and row1[on_attr] == row2[on_attr]:
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
    values = [row[attr] for row in table if attr in row and row[attr] is not None]
    if not values:
        return [{f"{func.upper()}({attr})": 0}]

    func = func.upper()
    if func == "SUM":
        return [{f"SUM({attr})": sum(values)}]
    elif func == "AVG":
        return [{f"AVG({attr})": sum(values) / len(values)}]
    elif func == "MIN":
        return [{f"MIN({attr})": min(values)}]
    elif func == "MAX":
        return [{f"MAX({attr})": max(values)}]
    elif func == "COUNT":
        return [{f"COUNT({attr})": len(values)}]
    else:
        raise ValueError(f"Unknown aggregate function: {func}")


def _split_args(args_str):
    args = []
    current_arg = ""
    paren_level = 0
    for char in args_str:
        if char == ',' and paren_level == 0:
            args.append(current_arg.strip())
            current_arg = ""
        else:
            if char == '(':
                paren_level += 1
            elif char == ')':
                paren_level -= 1
            current_arg += char
    args.append(current_arg.strip())
    return args

def execute_query(query):
    """
    Parses and executes a potentially nested relational algebra query.
    """
    query = query.strip()

    # Base Case: The query is a table name.
    if query in db:
        return db[query]

    # Recursive Step: The query is an operation.
    match = re.match(r"(\w+)\s*\((.*)\)", query, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid query format: {query}")

    operation = match.group(1).lower()
    args_str = match.group(2)
    
    args = _split_args(args_str)

    # --- Process operations ---

    if operation == "select":
        if len(args) != 2:
            raise ValueError("SELECT expects 2 arguments: condition and table.")
        condition = args[0]
        sub_table = execute_query(args[1])
        return select(sub_table, condition)
    
    elif operation == "project":
        if len(args) < 2:
            raise ValueError("PROJECT expects at least 2 arguments: one or more attributes and a table.")
        
        table_source = args[-1] 
        attributes_list = args[:-1]
        attributes_str = ",".join(attributes_list)
        
        sub_table = execute_query(table_source)
        return project(sub_table, attributes_str)

    elif operation == "join":
        if len(args) != 3:
            raise ValueError("JOIN expects 3 arguments: table1, table2, and on_attribute.")
        table1_name = args[0].strip()
        table2_name = args[1].strip()
        on_attr = args[2]
        table1 = execute_query(table1_name)
        table2 = execute_query(table2_name)
        return join(table1, table2, on_attr, table1_name, table2_name)

    elif operation in ["union", "intersect", "difference"]:
        if len(args) != 2:
            raise ValueError(f"{operation.upper()} expects 2 arguments: table1 and table2.")
        table1 = execute_query(args[0])
        table2 = execute_query(args[1])
        if operation == "union": return union(table1, table2)
        if operation == "intersect": return intersect(table1, table2)
        if operation == "difference": return difference(table1, table2)

    elif operation == "aggregate":
        if len(args) != 2:
            raise ValueError("AGGREGATE expects 2 arguments: function(attribute) and table.")
        
        # This regex now allows for dots in the attribute name (e.g., Table.Column)
        func_match = re.match(r"(\w+)\(([\w.]+)\)", args[0]) # <--- THIS LINE IS CHANGED
        
        if not func_match:
            raise ValueError("Invalid aggregate format. Expected FUNC(ATTRIBUTE), e.g., SUM(Salary).")
        func, attr = func_match.groups()
        sub_table = execute_query(args[1])
        return aggregate(sub_table, func, attr)
        
    else:
        raise ValueError(f"Unknown operation: {operation}")
if __name__ == "__main__":
    print("Relational Algebra Interpreter")
    print("Enter your query or type 'exit' to quit.")
    print("Example: project(Fname, select(Salary > 40000, EMPLOYEE))")
    
    while True:
        query = input(">> ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue
        try:
            result = execute_query(query)
            print_table(result)
        except Exception as e:
            print("Error:", e)