# XR-AI-Backend Setup

## Setting Up the Python Virtual Environment

To create a Python virtual environment, run the following command:

```sh
python3 -m venv .venv
```

### Activating the Virtual Environment

#### On macOS / Linux:

```sh
source .venv/bin/activate
```

#### On Windows:

```sh
.venv\Scripts\activate
```

## Installing / Updating Required Packages

### Install Required Packages

To install the required packages listed in the `requirements.txt` file, run:

```sh
pip install -r requirements.txt
```

### Update `requirements.txt`

If you've added or updated any dependencies, you can update the `requirements.txt` file by running:

```sh
pip freeze > requirements.txt
```

## Running the Project

To start the project locally, use the following command to launch the FastAPI application with Uvicorn:

```sh
uvicorn app.main:app --reload
```

This will run the server and automatically reload it for any code changes during development.

---

## Project Structure

Here is the basic directory structure of the project:

```
.  
├── app  
│   ├── api         # Contains all the API endpoints and routes  
│   ├── core        # Contains core configuration files, including environment variable loading and JWT handling  
│   ├── helpers     # Utility functions such as login manager, pagination logic  
│   ├── models      # Database models, integrated with Alembic for automatic migrations
│   ├── repositories  # Data access layer for interacting with the database  
│   ├── schemas     # Pydantic schemas for request and response validation  
│   ├── services    # CRUD operations and database interaction logic  
│   └── main.py     # Main entry point for configuring and running the application  
├── .gitignore      # Git ignore file to exclude unnecessary files from version control  
├── env.example     # Example environment configuration file  
├── logging.ini     # Logging configuration file  
├── README.md       # Project documentation file  
└── requirements.txt  # Contains a list of required Python packages  
```

---
