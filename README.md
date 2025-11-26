Public Policy Navigation System

A Machine Learning–powered Policy Categorization, Search, and Recommendation Tool

1. Project Overview

The Public Policy Navigation System is a FastAPI-based web application that helps users explore, classify, and analyze public policy documents across multiple domains such as Health, Education, and General governance.

It supports:

User registration & login

Policy uploads (CSV-based)

NLP-based policy categorization

TF–IDF vector search

Domain-specific policy browsing

Password reset workflow

A fully responsive UI

2. Folder Structure (Your Exact Structure)
PUBLIC_POLICY_CLEAN_FINAL/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── health.html
│   └── education.html
│
├── static/
│   └── (CSS / JS / Images as needed)
│
├── users.csv
├── education_policies.csv
├── test_policies.csv
├── train_policies.csv
├── indian_health_policies.csv
├── indian_health_policies_train.csv
├── indian_health_policies_test.csv
│
├── policy_vectorizer.pkl
├── policy_tfidf_matrix.pkl
├── health_policy_vectorizer.pkl
├── health_policy_tfidf_matrix.pkl
│
└── Notebooks (for training)
    ├── infosys_health_nlp.ipynb
    └── infosys_nlp.ipynb

What Each File Does
app.py

Main FastAPI server:

Manages authentication system (login/register/forgot-password)

Serves templates

Loads ML models

Performs policy search using TF–IDF

Renders domain-based results

templates/

Contains all HTML templates for the website:

login.html — Login screen

register.html — New user signup

forgot_password.html — Reset password

index.html — Homepage/dashboard

health.html — Health policy results

education.html — Education policy results

static/

Front-end assets (CSS/JS/Images).
Controls the UI styling and interaction.

policy_vectorizer.pkl / policy_tfidf_matrix.pkl

Stored ML model files for general policy search.

health_policy_vectorizer.pkl / health_policy_tfidf_matrix.pkl

Domain-specific ML model for Health policies.

CSV Datasets

train_policies.csv / test_policies.csv — Generic policy dataset

indian_health_policies*.csv — Health policy dataset

education_policies.csv — Education domain dataset

users.csv — Stores registered user details

Jupyter Notebooks

Used for training and generating:

Vectorizers

TF–IDF matrices

Preprocessing steps

3. Features
User Authentication

Register

Login

Reset password

CSV-based user storage

Policy Search

TF–IDF similarity search

Instant relevance score

Domain-specific results for Health & Education

Policy Dashboard

List all policies

Filter by domain

Clean UI

Machine Learning

Pre-trained vectorizers

TF–IDF matrices

Policy similarity search

CSV datasets for training/testing

4. How It Works
Step 1: User logs in

users.csv is used to validate credentials.

Step 2: User chooses policy domain

You provide:

Health

Education

All Policies

Step 3: FastAPI loads:

Vectorizer (.pkl)

TF–IDF matrix (.pkl)

CSV dataset

Step 4: Search Flow

Convert query → vector with same vectorizer

Cosine similarity against TF–IDF matrix

Top results returned

Rendered in HTML template

5. How to Run the Project
Install dependencies
pip install -r requirements.txt

Start the server
uvicorn app:app --reload

Open in browser:
http://127.0.0.1:8000

6. Requirements

Works on Python 3.8+
Requires:

FastAPI

Uvicorn

Pandas

Scikit-learn

Jinja2

Numpy

7. Notes

Both policy and health vectorizers must stay in the project root.

CSV files must not be renamed.

Password reset modifies users.csv.

Notebooks are only for training, not required for running the server.

8. Future Enhancements (Optional)

JWT-based authentication

Database (PostgreSQL) instead of CSV

Policy upload by users

Dashboard analytics

Role-based access