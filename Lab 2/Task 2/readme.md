Of course. Here is a comprehensive README file for your Python script, explaining how it works and detailing the syntax for each query.

Simple Relational Algebra Query Engine

This script is a command-line tool that simulates a basic database query engine. It loads data from a local JSON file and allows you to perform core relational algebra operations like SELECT, PROJECT, JOIN, and more using a simple, text-based syntax.

⚙️ Prerequisites

1. Python

Ensure you have Python 3 installed on your system. This script uses standard libraries (json, re) and does not require any external packages to be installed.

2. Data File

The script requires a JSON file named company.json to be in the same directory. This file should contain a single JSON object where each key is a "table name" and its value is an array of objects (the "rows").

Example company.json:
JSON

{
  "Employee": [
    {"SSN": 1, "Name": "Ali", "DeptID": 10, "Salary": 5000},
    {"SSN": 2, "Name": "Mona", "DeptID": 20, "Salary": 6000},
    {"SSN": 3, "Name": "Omar", "DeptID": 10, "Salary": 7000}
  ],
  "Employee2":
  [
    {"SSN": 1, "Name": "Ali", "DeptID": 10, "Salary": 5000},
    {"SSN": 2, "Name": "Mona", "DeptID": 20, "Salary": 6000},
    {"SSN": 4, "Name": "Sara", "DeptID": 30, "Salary": 8000},
    {"SSN": 5, "Name": "Hana", "DeptID": 40, "Salary": 9000},
    {"SSN": 6, "Name": "Lina", "DeptID": 50, "Salary": 10000}
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

    An interactive prompt will appear. You can now type your queries.

📖 Query Reference

Here are the supported operations and their syntax. All keywords are case-sensitive.

🔍 SELECT

Filters rows from a single table based on a condition.

    Syntax: SELECT <table_name> WHERE <condition>

    Details: The <condition> is a standard Python boolean expression. You can use the column names as variables within the condition. Standard Python operators like ==, >, <, >=, <=, and, or, not are supported. String values must be enclosed in quotes (e.g., 'John').

    Example:

    SELECT Employee WHERE Salary > 55000 and DeptID == 5

✨ PROJECT

Selects a subset of columns (attributes) from a table.

    Syntax: PROJECT <attribute1>, <attribute2> FROM <table_name>

    Details: Provide a comma-separated list of the column names you want to display.

    Example:

    PROJECT SSN,Name,Salary FROM employees

🔗 JOIN

Combines rows from two tables based on a common attribute value (an inner join).

    Syntax: JOIN <table1>,<table2> ON <common_attribute>

    Details: The resulting table will have column names prefixed with their original table names (e.g., employees.Fname, departments.Dname).

    Example:

    JOIN Employee,Department ON DeptID



∪ UNION

Combines the rows of two tables and removes any duplicates.

    Syntax: UNION <table1>,<table2>

    Details: The two tables should have identical column structures for the union to be meaningful.

    Example:

    UNION Employee,Employee1

∩ INTERSECT

Returns only the rows that exist in both tables.

    Syntax: INTERSECT <table1>,<table2>

    Details: Like UNION, this works best when the tables have identical structures.

    Example:

    INTERSECT Employee,Employee1

− DIFFERENCE

Returns rows that are in the first table but not in the second table.

    Syntax: DIFFERENCE <table1>,<table2>

    Example:

    DIFFERENCE Employee,Employee1

∑ AGGREGATE

Performs a calculation on a single column, returning a single value.

    Syntax: AGGREGATE <FUNCTION>(<attribute>) FROM <table_name>

    Supported Functions: SUM, AVG, MIN, MAX, COUNT.

    Example:

    AGGREGATE AVG(Salary) FROM Employee

    AGGREGATE COUNT(SSN) FROM Employee

🚪 Exiting the Program

To stop the script and exit the interactive prompt, type exit and press Enter.

exit