# Queueing Web System (Django)

A starter Django app that lets users take queue tickets and admins manage the queue.

## Features
- Users: take ticket, view status, see position
- Admins (staff): call next, mark served, skip, reset today
- Uses Django auth, Bootstrap UI, SQLite by default

## Quickstart

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- User: http://127.0.0.1:8000/
- Admin site: http://127.0.0.1:8000/admin/
- Staff dashboard: http://127.0.0.1:8000/admin/dashboard/

> Make your superuser **staff** via Django admin if not already.

## Notes
- Tickets reset each day (numbers are unique per day).
- Time zone is set to `Asia/Manila` in settings.
- For production, set `DJANGO_SECRET_KEY` and turn off `DEBUG`.
