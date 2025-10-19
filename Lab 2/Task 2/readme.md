Simple Relational Algebra Query Engine

This script is a command-line tool that simulates a basic database query engine. It loads data from a local JSON file and allows you to perform core relational algebra operations like select, project, join, and more using a simple, function-based syntax.

The key feature of this engine is its ability to nest operations, allowing you to create complex queries by feeding the result of one operation directly into another.

⚙️ Prerequisites

    Python Ensure you have Python 3 installed on your system. This script uses standard libraries (json, re) and does not require any external packages.

    Data File The script requires a JSON file named company.json to be in the same directory. This file should contain a single JSON object where each key is a "table name" and its value is an array of objects (the "rows").

    Example company.json:
    JSON

    {
      "Employee": [
        {"SSN": 1, "Name": "Ali", "DeptID": 10, "Salary": 50000},
        {"SSN": 2, "Name": "Mona", "DeptID": 20, "Salary": 60000},
        {"SSN": 3, "Name": "Omar", "DeptID": 10, "Salary": 70000}
      ],
      "Employee2": [
        {"SSN": 1, "Name": "Ali", "DeptID": 10, "Salary": 50000},
        {"SSN": 4, "Name": "Sara", "DeptID": 30, "Salary": 80000}
      ],
      "Department": [
        {"DeptID": 10, "Name": "IT"},
        {"DeptID": 20, "Name": "HR"}
      ]
    }

▶️ How to Run

    Save the script as main.py.

    Create your company.json file in the same directory.

    Run the script from your terminal:
    Bash

    python3 main.py

    An interactive prompt >> will appear. You can now type your queries.

🚀 Nested Queries

The most powerful feature of this engine is the ability to combine operations. You can use any query as an argument for another query's table source.

Example: Find the names and salaries of employees who earn more than 55,000.

>> project(Name, Salary, select(Salary > 55000, Employee))

How it works:

    The inner select(Salary > 55000, Employee) runs first.

    It returns a temporary, in-memory table containing only the employees who meet the salary condition.

    This temporary table is then passed as the input to the project operation, which selects the Name and Salary columns.

📖 Query Reference

Here are the supported operations and their syntax. All operation keywords (select, project, etc.) are case-insensitive.

🔍 select

Filters rows from a single table based on a condition.

    Syntax: select(<condition>, <table_source>)

    Details: The <condition> must be enclosed in single or double quotes. It is a standard Python boolean expression where you can use column names as variables. String values within the condition must also be quoted (e.g., 'Name == "Ali"'). The <table_source> can be a table name or another query.

    Example:

    >> select('Salary > 55000 and DeptID == 10', Employee)

✨ project

Selects a subset of columns (attributes) from a table.

    Syntax: project(<attribute1>, <attribute2>, ..., <table_source>)

    Details: Provide one or more comma-separated column names you want to display. The last argument must be the <table_source>.

    Example:

    >> project(SSN, Name, Salary, Employee)

🔗 join

Combines rows from two tables based on a common attribute value (an inner join).

    Syntax: join(<table1>, <table2>, <common_attribute>)

    Details: The resulting table will have column names prefixed with their original table names (e.g., Employee.Name, Department.Name). The <common_attribute> should not be in quotes.

    Example:

    >> join(Employee, Department, DeptID)

∪ union

Combines the rows of two tables and removes any duplicates.

    Syntax: union(<table_source1>, <table_source2>)

    Details: The two tables should have identical column structures for the union to be meaningful.

    Example:

    >> union(Employee, Employee2)

∩ intersect

Returns only the rows that exist in both tables.

    Syntax: intersect(<table_source1>, <table_source2>)

    Details: Like union, this works best when the tables have identical structures.

    Example:

    >> intersect(Employee, Employee2)

− difference

Returns rows that are in the first table but not in the second.

    Syntax: difference(<table_source1>, <table_source2>)

    Example:

    >> difference(Employee, Employee2)

∑ aggregate

Performs a calculation on a single column, returning a single value.

    Syntax: aggregate(<FUNCTION>(<attribute>), <table_source>)

    Supported Functions: SUM, AVG, MIN, MAX, COUNT.

    Example:

    >> aggregate(AVG(Salary), Employee)
    >> aggregate(COUNT(SSN), select(Salary > 60000, Employee))

🚪 Exiting the Program

To stop the script and exit the interactive prompt, type exit and press Enter.

>> exit