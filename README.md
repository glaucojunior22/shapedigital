# Test Description 
## The assignment involves creating a backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading).
## This system will be used for other applications in the organization and we should have APIs with the appropriate HTTP request methods to be able to reuse them.

### The data should be stored in the database.

### The main functionalities of this software are:

1. Registering a vessel. The vessel data input is its code, which can’t be repeated (return the HTTP code appropriate and an error
message if the user tries to register an existing code). For instance, a valid input of a vessel is:“code”:“MV102”.

2. Registering a new equipment in a vessel. The data inputs of each equipment are name, code, location and status. Each equipment is
associated to a given vessel and has a unique code, which can’t be repeated (return the HTTP code appropriate and an error message if
the user tries to register a existing code). For each new equipment registered, the equipment status is automatically active. For instance, a
valid input of a new equipment related to a vessel “MV102”is: { "name": "compressor", "code": "5310B9D7", "location": "Brazil" }

3. Setting an equipment’s status to inactive. The input data should be one or a list of equipment code.

4. Returning all active equipment of a vessel Feel free to use the programming language and tools you would like.

5. Add an operation order with a cost to a equipment. For instance, a valid input of a new operation related to a equipment “5310B9D7”
is: {"code": "5310B9D7", type: "replacement", "cost": "10000"}

6. Return the total cost in operation of an equipment by code.

7. Return the total cost in operation of a set of equipments by name.

8. Return the average cost in operation in each vessel.

### The project should be easy deployable, easy to understand, have good test coverage and be easy to expand.

### Once you’re done, put your code in a repository and send us the link to it with a document explaining step by step the technologies used and how to run your code.

### We will evaluate:

1. Best practices on how you design your solution

2. Unit tests are mandatory

3. Software engineering principles:API design, separation of concerns and modularity

# How to run this project

## Without Docker

1. Clone this repo on your machine

2. Create a virtualenv with python 3.9+ with command: `python -m venv .venv`

3. Activate the virtualenv: `source .venv/bin/activate`

4. Instal the dependencies using the command: `pip install -r requirements.txt`

5. Run the server with the command: `uvicorn app.main:app --reload`

### To run the tests:

1. Enter the app directory: `cd app`

2. Run Pytest: `pytest`

## With Docker

## You need to have Docker engine installed: [Install Docker](https://docs.docker.com/engine/install/)

1. build the Docker Image: `sudo docker build -t shapedigital .`

2. Run the Docker container: `sudo docker run -dp 8000:8000 shapedigital`

- The default port is 8000, so access the API docs using: [Docs](http://localhost:8000/docs) or [Redoc](http://localhost:8000/redoc)

# Tecnologies used for the project
- Python (programming language)
- FastAPI (API Framework)
- Pydantic (Models Serialization/Data Validation)
- SqlAlchemy (Database ORM)
- Pytest (Tests Framework)
- SQLite (Database for development, can be easily changed on file app.db line 5)