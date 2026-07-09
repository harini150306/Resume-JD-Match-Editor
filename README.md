# AI-Powered Resume-JD Matcher

## Overview

The AI-Powered Resume-JD Matcher is a web application that analyzes a candidate's resume against a job description (JD) to determine how well the candidate's profile matches the role requirements. The system extracts skills, identifies missing competencies, calculates a match score, and provides recommendations to improve the candidate's chances of passing Applicant Tracking Systems (ATS).

---

## Features

* Upload and parse resumes in PDF format.
* Upload or paste a job description.
* Extract technical skills and keywords from resumes and JDs.
* Calculate Resume-to-JD match percentage.
* Identify missing skills required for the role.
* Generate recommendations to improve ATS compatibility.
* User authentication using JWT tokens.
* Secure API endpoints with token-based authorization.
* RESTful API built with FastAPI.

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite / MySQL
* JWT Authentication
* Pydantic

### Libraries

* python-jose
* passlib
* python-multipart
* PyPDF2 / pdfplumber
* Uvicorn

### Tools

* Git
* GitHub
* Postman
* VS Code

---

## Project Structure

```text
resume-jd-matcher/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   ├── dependencies.py
│   └── main.py
│
├── uploads/
├── requirements.txt
├── README.md
└── .env
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/resume-jd-matcher.git
cd resume-jd-matcher
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Authentication

* `POST /register` - Register a new user
* `POST /login` - Login and receive JWT token

### Resume Parsing

* `POST /parse-resume` - Upload and extract resume content

### Job Description Analysis

* `POST /match-jd` - Compare resume with job description
* `GET /match-score` - Retrieve match score and analysis

---

## Workflow

1. User registers and logs into the system.
2. User uploads a resume.
3. User uploads or enters a job description.
4. The system extracts skills and keywords from both documents.
5. Matching algorithms compare the two datasets.
6. A match score is generated.
7. Missing skills and recommendations are displayed to the user.

---

## Future Enhancements

* AI-generated ATS-optimized resume generation.
* Learning roadmap for missing skills.
* Support for multiple resume formats.
* Job recommendation engine.
* Dashboard with analytics and reports.
* Resume version management.

---

## Use Cases

* Students applying for placements.
* Job seekers optimizing resumes.
* Recruiters performing preliminary screening.
* Career guidance and skill gap analysis.

---

## Author

**Harini H**

Final Year B.E. Computer Science Engineering Student

KGiSL Institute of Technology

GitHub: https://github.com/harini150306
