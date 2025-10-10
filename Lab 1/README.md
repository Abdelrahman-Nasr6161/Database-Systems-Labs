# Project Overview

This project is divided into three main files:

- **task1.py**  
    Responsible for reading JSON data from `data.json` and using the `dbis-er-diagram` library to parse the JSON into an ER diagram, which is saved as a PNG image.

- **task2.py**  
    Utilizes a Google Gemini API key to send a carefully engineered prompt to Gemini, generating a `data.json` file in the required format for `task1.py`.

- **runner.sh**  
    A shell script that runs the end-to-end workflow by executing `task2.py` followed by `task1.py`.

## How to Run
- First, create and activate a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

- Then, install the required packages:
    ```
    pip install -r requirements.txt
    ```
- To generate the ER diagram from an existing `data.json`:
    ```
    python3 task1.py
    ```

- To generate a new `data.json` using Gemini:
    ```
    python3 task2.py
    ```
* Note: For security reasons, the API key is not included in this code sample because it is hosted on GitHub.
- To run the entire process (generate `data.json` and then the ER diagram):
    ```
    ./runner.sh
    ```