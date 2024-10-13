
# Library Management System API

## Introduction

This project is a **Library Management System API** built using **FastAPI**, **SQLAlchemy**, and **Alembic**. The API handles the management of users, books, authors, genres, and book rentals. Users can borrow and return books, while administrators can manage the library's inventory.

The project integrates with an **Oracle Database**, and uses **SonarQube** for code quality checks. A frontend is also available for the project.

## Installation

### 0. Requirements

To install the required Python libraries, run the following command:

```bash
pip install -r requirements.txt
```

### 1. Create `.env` file

In the root directory of the project, create a `.env` file with the following environment variables. This file will store your Oracle database credentials and other necessary configurations.

```env

DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_DSN=

DATABASE_TABLE=SCHEMA.TABLE_NAME

SQLALCHEMY_DATABASE_URL=


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```



### 2. Run Alembic Migrations

To set up the database schema, you will need to run Alembic migrations. These migrations will create the necessary tables for users, books, authors, genres, and rentals.

Run the following command to apply the migrations:

IF you modified models : 


```bash
alembic revision --autogenerate -m "Add Status to Rents "
```

To run migration 

```bash
alembic upgrade head
```




### 3. Insert Fake Data from Kaggle

To insert initial data into the database for testing purposes, run the `data.py` script. This script will pull fake data from Kaggle datasets (like books, authors, and genres) and insert them into the database.


```bash
cd app/
python3 data.py
```

### 4. Workflow with SonarQube

This project integrates **SonarQube** for continuous code quality checks. The workflow for running SonarQube is already set up in the project.

Make sure the configuration in `sonar-project.properties` is correctly set up to point to your SonarQube server.

AND add keys in GITHUB WORKFLOW CONFIG



## How to Run the Application


 **Start the FastAPI server:**

   Run the server on your local machine with:

   ```bash
   fastapi dev main.py   
   ```

 **Access the API documentation:**

   Once the server is running, you can access the interactive API documentation by navigating to:

   [http://localhost:8000/docs](http://localhost:8000/docs)



## Conclusion

This API provides a complete solution for managing a library system, including managing books, users, and rentals. It supports an Oracle database and integrates with SonarQube for code quality assurance.

```

