# Credit Approval Application

The **Credit Approval Application** is a Django-based system to handle customer registration, loan eligibility checks, and loan management. It offers REST APIs to perform all operations and is containerized using Docker for ease of deployment.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Setup](#setup)
4. [Running the Application](#running-the-application)
   - [Without Docker](#without-docker)
   - [With Docker](#with-docker)
5. [API Endpoints](#api-endpoints)
6. [Sample API Usage](#sample-api-usage)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

---

## Requirements

- **Python**: 3.10 or higher
- **Docker**: Latest version
- **Docker Compose**: Installed and configured
- **Postman** (optional): For API testing
- **Curl** (optional): For API testing

---

## Installation

1. **Clone the Repository**:

    ```bash
    git clone <repository-url>
    cd credit_approvel_app
    ```

2. **Create a Virtual Environment (Optional)**:

    ```bash
    python3.10 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

---

## Setup

### Database Configuration

- **Docker**: Uses PostgreSQL container (see `docker-compose.yml` for details).
- **Non-Docker**: Configure your database in `credit_approvel_app/settings.py` under the `DATABASES` section.

Apply migrations to initialize the database:

```bash
python manage.py migrate
```

---

## Running the Application

### Without Docker

1. Start the server:

    ```bash
    python manage.py runserver
    ```

2. Access the application at `http://127.0.0.1:8000/`.

---

### With Docker

1. **Build and Start Containers**:

    ```bash
    docker-compose up --build
    ```

2. Access the application at `http://127.0.0.1:8000/`.

3. **Manage the Docker Containers**:
   - Stop containers: `docker-compose down`
   - View logs: `docker-compose logs -f`
   - Rebuild containers: `docker-compose up --build`

---

## API Endpoints

| Method | Endpoint                                | Description                                       |
|--------|-----------------------------------------|---------------------------------------------------|
| POST   | `/api/register/`                        | Register a new customer                          |
| POST   | `/api/check-eligibility/`               | Check if a customer is eligible for a loan       |
| POST   | `/api/create-loan/`                     | Create a loan for a customer                     |
| GET    | `/api/view-loan/<int:loan_id>/`         | Fetch details of a loan with a specific ID       |
| GET    | `/api/view-loans/<int:customer_id>/`    | Fetch all loans associated with a specific user  |

---

## Sample API Usage

### 1. **Register a Customer**

**Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Alice Smith",
    "email": "alice.smith@example.com",
    "phone_number": "9876543210"
}'
```

**Response**:

```json
{
    "id": 1,
    "name": "Alice Smith",
    "email": "alice.smith@example.com",
    "phone_number": "9876543210",
    "message": "Customer registered successfully"
}
```

---

### 2. **Check Loan Eligibility**

**Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/check-eligibility/ \
-H "Content-Type: application/json" \
-d '{
    "customer_id": 1,
    "loan_amount": 50000,
    "loan_duration_months": 24
}'
```

**Response**:

```json
{
    "customer_id": 1,
    "is_eligible": true,
    "eligible_amount": 50000,
    "message": "Customer is eligible for the requested loan"
}
```

---

### 3. **Create a Loan**

**Request**:

```bash
curl -X POST http://127.0.0.1:8000/api/create-loan/ \
-H "Content-Type: application/json" \
-d '{
    "customer_id": 1,
    "loan_amount": 50000,
    "loan_duration_months": 24
}'
```

**Response**:

```json
{
    "loan_id": 1,
    "customer_id": 1,
    "loan_amount": 50000,
    "loan_duration_months": 24,
    "message": "Loan created successfully"
}
```

---

### 4. **Fetch Loan Details**

**Request**:

```bash
curl -X GET http://127.0.0.1:8000/api/view-loan/1/
```

**Response**:

```json
{
    "loan_id": 1,
    "customer_id": 1,
    "loan_amount": 50000,
    "loan_duration_months": 24,
    "status": "Active"
}
```

---

### 5. **Fetch All Loans for a Customer**

**Request**:

```bash
curl -X GET http://127.0.0.1:8000/api/view-loans/1/
```

**Response**:

```json
[
    {
        "loan_id": 1,
        "loan_amount": 50000,
        "loan_duration_months": 24,
        "status": "Active"
    },
    {
        "loan_id": 2,
        "loan_amount": 100000,
        "loan_duration_months": 36,
        "status": "Pending"
    }
]
```

---

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   Ensure the database is running and the credentials in `settings.py` match.

2. **Port Already in Use**:
   Update the `ports` in `docker-compose.yml`:

   ```yaml
   ports:
     - "8080:8000"
   ```

3. **Docker Build Fails**:
   Rebuild the containers:

   ```bash
   docker-compose up --build
   ```

---

## Contributing

We welcome contributions! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add feature'`.
4. Push the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---