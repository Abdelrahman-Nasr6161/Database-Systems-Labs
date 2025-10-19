Database Schema Visualizer

This project uses Python to automatically generate a database schema diagram from a JSON configuration file.

⚙️ Installation

To run this script, you first need to set up a virtual environment and install the necessary dependencies.

1. Create and Activate a Virtual Environment

A virtual environment keeps your project dependencies isolated.
Bash

# Create the virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
.\venv\Scripts\activate

2. Install Requirements

This project's dependencies are listed in the requirements.txt file.
Bash

pip install -r requirements.txt

    Note: eralchemy requires GraphViz to be installed on your system. Please follow the installation instructions for your operating system from the official GraphViz website.This will specifically cause an issue if this is tested on Windows because you need to manually add GraphViz to your PATH

🚀 How It Works

This script leverages the eralchemy library to automatically generate a Relational Model Visualization from an ERD Schema JSON Representation.

eralchemy is built on top of two powerful tools:

    GraphViz: An open-source graph visualization software used to render the final diagram.

    SQLAlchemy: A SQL toolkit and Object-Relational Mapper (ORM) that describes the database structures in Python.

The script follows these steps:

    It reads the database schema definitions from the data.json file.

    It uses this information to dynamically construct SQLAlchemy models.

    The collection of these models (the SQLAlchemy Base) is passed to eralchemy.

    eralchemy processes the Base to create a Relational Model Diagram, which is then saved as output.png.

▶️ Usage

Once the setup is complete, you can generate the diagram by running the main.py script:
Bash

python3 main.py

This command will execute the script and generate the output.png file in your project's root directory.

