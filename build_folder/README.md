# Rajaro Solutions Website

Full-stack website for **Rajaro Solutions Private Limited** built from the design PDF, with Jinja2 templates, HTMX form submissions, and an admin panel for content management.

## Features

### Public Site
- **Home** — Hero, promises, service highlights
- **About Us** — Mission, vision, clients, founder, why choose us
- **Services** — 9 service categories with expertise lists + consultation booking form
- **Products** — Subitra & RajaroRise with pricing tables
- **Learning Center** — Courses, webinars, events
- **Referral Program** — Affiliate info + application form
- **Contact** — Contact form + company details
- **Career** — Job listings with full hiring & internship application forms (resume upload)
- **Blog** — Posts with full view
- **Notifications** — Site announcements
- **Search** — Jobs, blogs, services

### Admin Panel (`/admin`)
- Dashboard with stats
- Edit all site content, hero promises
- Manage services, products & pricing
- About page (clients, why choose items)
- Learning, affiliate program content
- View contact submissions, consultations, affiliate applications
- Job CRUD + application review (status, notes, resume download)
- Blog CRUD
- Notifications management

## Quick Start

```bash
cd Monish_website
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

### Admin Login
- URL: **http://127.0.0.1:5000/admin**
- Default username: `admin`
- Default password: `admin123`

Change credentials via environment variables:
```
ADMIN_USERNAME=youruser
ADMIN_PASSWORD=yourpassword
SECRET_KEY=your-secret-key
```

## Tech Stack
- **Flask** + **Jinja2** — Server-rendered pages
- **HTMX** — Async form submissions without page reload
- **SQLite** — Database (auto-created on first run)
- **Flask-Login** — Admin authentication
