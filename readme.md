# CREDIT APPROVEL SYSTEM

This repository contains the source code for the **Credit Approval Application**. The project is built using Django and Django REST Framework (DRF) and allows customers to register, check loan eligibility, create loans, and manage loan details.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
  - [Example Usage](#example-usage)
- [Troubleshooting](#troubleshooting)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

To run this project, ensure you have the following:

- **Python**: 3.10 or later
- **Django**: 5.x or later
- **Django REST Framework**: Installed via `requirements.txt`
- **PostgreSQL**: For database support
- **HTTP Client**: Tools like [Postman](https://www.postman.com/) or `curl` for testing APIs.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd credit_approvel_app
```

### 2. Create a Virtual Environment

```bash
python3.10 -m venv venv
venv\Scripts\activate   #On Linux : source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Update the `DATABASES` section in `settings.py` with your PostgreSQL credentials.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Start the Server

```bash
python manage.py runserver
```

---

## Running the Project

Once the server is running, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the application.

---

## API Endpoints

Here is a list of the available API endpoints:

| Method | Endpoint                          | Description                                  |
|--------|-----------------------------------|----------------------------------------------|
| POST   | `/api/register/`                  | Register a customer                          |
| POST   | `/api/check-eligibility/`         | Check eligibility for a loan                 |
| POST   | `/api/create-loan/`               | Create a loan                                |
| GET    | `/api/view-loan/<int:loan_id>/`   | Fetch details of a loan with loan ID         |
| GET    | `/api/view-loans/<int:customer_id>/` | Fetch all loans for a specific customer       |

---

## Example Usage

Here are examples of how to use the APIs. Replace `<host>` with `127.0.0.1:8000` for local development.

---

### 1. Register a Customer (POST `/api/register/`)

#### Request:

```bash
curl -X POST <host>/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "9876543210"
}'
```

#### Response:

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "9876543210",
    "message": "Customer registered successfully"
}
```

---

### 2. Check Loan Eligibility (POST `/api/check-eligibility/`)

#### Request:

```bash
curl -X POST <host>/api/check-eligibility/ \
-H "Content-Type: application/json" \
-d '{
    "customer_id": 1,
    "income": 50000,
    "credit_score": 750
}'
```

#### Response:

```json
{
    "is_eligible": true,
    "message": "Customer is eligible for a loan"
}
```

---

### 3. Create a Loan (POST `/api/create-loan/`)

#### Request:

```bash
curl -X POST <host>/api/create-loan/ \
-H "Content-Type: application/json" \
-d '{
    "customer_id": 1,
    "loan_amount": 200000,
    "tenure_months": 24,
    "interest_rate": 7.5
}'
```

#### Response:

```json
{
    "loan_id": 101,
    "message": "Loan created successfully"
}
```

---

### 4. View a Loan (GET `/api/view-loan/<int:loan_id>/`)

#### Request:

```bash
curl -X GET <host>/api/view-loan/101/ \
-H "Content-Type: application/json"
```

#### Response:

```json
{
    "loan_id": 101,
    "customer_id": 1,
    "loan_amount": 200000,
    "tenure_months": 24,
    "interest_rate": 7.5,
    "status": "Active"
}
```

---

### 5. View All Loans for a Customer (GET `/api/view-loans/<int:customer_id>/`)

#### Request:

```bash
curl -X GET <host>/api/view-loans/1/ \
-H "Content-Type: application/json"
```

#### Response:

```json
[
    {
        "loan_id": 101,
        "loan_amount": 200000,
        "tenure_months": 24,
        "interest_rate": 7.5,
        "status": "Active"
    },
    {
        "loan_id": 102,
        "loan_amount": 150000,
        "tenure_months": 18,
        "interest_rate": 6.8,
        "status": "Closed"
    }
]
```

---

## Troubleshooting

### Python Version Issue

If you encounter the error:

```
ERROR: No matching distribution found for Django==5.x
```

Ensure your Python version is 3.10 or later. Upgrade Python and recreate your virtual environment.

### Database Connection Issue

Ensure that your database credentials are correct in `settings.py` and that PostgreSQL is running.

---

## Features

- Customer registration and management
- Loan eligibility checks
- Loan creation and tracking
- View specific loans or all loans for a customer
- Scalable and extensible REST API

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature-name'`.
4. Push the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).
