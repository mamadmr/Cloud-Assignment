
# Web API for Secure CTF Flag Storage 🏁

This repository contains a Flask-based web API designed to **securely store and retrieve flags** in a Capture The Flag (CTF) environment. The system is built to interact with two essential services: a **PostgreSQL** database for persistent storage and a **Redis** server for temporary in-memory data operations.

---

## 🧠 Problem Description

Design and implement a **web API** with two main endpoints:

- `POST /flags`  
  - Accepts a `flag` and `user` in the JSON body.
  - Validates that the flag starts with `FLAG-`.
  - Stores the flag into a **PostgreSQL** database with the associated user.

- `GET /flags/<user>`  
  - Retrieves the last submitted flag for the specified user from **Redis** (cache).

### 🔐 Security Requirement

- Flags must only be accepted if they begin with `FLAG-`.
- Invalid flags should return an appropriate error response.
- Redis is used to cache the latest flag per user for fast retrieval.

---

## 🚀 Technology Stack

- **Python 3.12**
- **Flask** for API handling
- **PostgreSQL** for persistent flag storage
- **Redis** for fast flag retrieval (caching)
- **Docker + Docker Compose** for containerized environment

---

## 🛠️ Setup Instructions

### 📦 Requirements

- Docker & Docker Compose installed
- Python 3.12 & `venv` (for local Python development)

---

## 🔧 Step-by-Step Usage

### 1. Clone the Repository

```bash
git clone 
cd 
````

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Services Using Docker Compose

```bash
docker-compose up -d
```

This command will spin up:

* `db` (PostgreSQL on port `5432`)
* `redis` (Redis on port `6379`)

> If Redis fails to start due to port conflicts, make sure port `6379` is not used by another Redis instance.

---

### 5. Set Environment Variables

Create a `.env` file (or export manually):

```env
DATABASE_URL=postgresql://ctf_user:admin123@localhost:5432/ctf_db
REDIS_URL=redis://localhost:6379/0
```

In Linux/Mac:

```bash
export DATABASE_URL=postgresql://ctf_user:admin123@localhost:5432/ctf_db
export REDIS_URL=redis://localhost:6379/0
```

---

### 6. Run the Web Server

```bash
python run.py
```

The API will be available at: `http://localhost:5000`

---

## 🧪 API Usage

### ➕ POST `/flags`

**Request:**

```http
POST /flags
Content-Type: application/json

{
  "user": "alice",
  "flag": "FLAG-CTF123"
}
```

**Response:**

```json
{
  "message": "Flag stored successfully."
}
```

---

### 🔍 GET `/flags/<user>`

**Request:**

```http
GET /flags/alice
```

**Response:**

```json
{
  "user": "alice",
  "flag": "FLAG-CTF123"
}
```

---

## 🧼 Clean Up

To stop and remove the containers:

```bash
docker-compose down
```
