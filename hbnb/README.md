# HBnB Evolution - Backend API

This project is a modular Flask-based REST API for an AirBnB-like app.

## Directory Structure

- `app/api/v1/`: REST API endpoints (Flask-RESTx)
- `app/models/`: Business logic entities
- `app/services/`: Facade connecting API to logic
- `app/persistence/`: In-memory storage (will be replaced with SQLAlchemy)
- `config.py`: Environment config
- `run.py`: App entry point

## Setup

Install requirements:

```bash
pip install -r requirements.txt
