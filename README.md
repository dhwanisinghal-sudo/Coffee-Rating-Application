# Coffee Rating Application

A full-stack coffee voting application built with Python Flask, SQLite, HTML, CSS, and JavaScript.

## Features
- Displays a list of coffee items with descriptions and vote totals.
- Each Vote button sends a POST request to the Flask backend.
- Backend increments the selected coffee's vote count in SQLite.
- Updated counts are fetched and displayed on the page.
- Vote totals remain saved after refreshing or restarting the application.

## Run in VS Code (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/coffees` | Get coffee items and vote totals |
| POST | `/api/coffees/<id>/vote` | Add one vote to a coffee item |
