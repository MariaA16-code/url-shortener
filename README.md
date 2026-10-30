# URL Shortener

## Overview
Built this to learn how URL routing and database lookups work together
in a backend application.

## Tech Stack
- Python, Flask
- PostgreSQL (Supabase), SQLAlchemy
- HTML, CSS, JavaScript
- Deployed on Render

## Features
- Shorten any URL
- Click tracking
- Delete links

## Run Locally
```bash
pip install -r requirements.txt
```

Create a `.env` file in the project folder:
```
DATABASE_URL=your_postgresql_connection_string
```

Then run:
```bash
python app.py
```
Without `DATABASE_URL`, the app falls back to a local SQLite database.

## Live demo
View on Render: https://url-shortener-1yb1.onrender.com

Note: hosted on a free tier, so the first load after inactivity can take about 30 to 60 seconds.