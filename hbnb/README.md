# HBnB Evolution - Backend API

This project is a modular Flask-based REST API for an AirBnB-like app.

## Directory Structure

- `app/api/v1/`: REST API endpoints (Flask-RESTx)
- `app/models/`: Business logic entities
- `app/services/`: Facade connecting API to logic
- `app/persistence/`: In-memory storage (will be replaced with SQLAlchemy)
- `config.py`: Environment config
- `run.py`: App entry point


## Business Logic

Core entity classes:

- **User**: first_name, last_name, email, is_admin
- **Place**: title, price, location, owned by User, can have Reviews and Amenities
- **Review**: text and rating, linked to a Place and User
- **Amenity**: e.g. "Wi-Fi", associated with Places

All classes inherit from BaseModel, which manages `id`, `created_at`, and `updated_at`.

## Setup

#### Install requirements:

```bash
pip install -r requirements.txt
```

#### Run the app:

```bash
python run.py
