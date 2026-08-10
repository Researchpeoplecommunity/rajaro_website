# Rajaro Solutions Website

Full-stack website for **Rajaro Solutions Private Limited** with Jinja2 templates, HTMX forms, searchable product/service selectors, and a full admin CMS.

## Public Site

| Page | URL | Notes |
|------|-----|-------|
| Home | `/` | Curiosity-driven gateway to all sections |
| About Us | `/about` | Scannable mission, vision, clients, founder |
| Services | `/services` | Technology + digital marketing cards, book consultation |
| Products | `/products` | Subitra & RajaroRise — View More (no public pricing) |
| Learning Program | `/learning` | Programs with CTA links |
| Contact | `/contact` | Form with searchable product/service selector |
| Suggestions | `/suggestions` | Feedback form + PDF upload |
| Career | `/career` | Job listings + apply (hiring & internship) |
| Blog | `/blog` | Articles with featured images |
| Search | `/search` | Jobs, blogs, services |

## Admin Panel (`/admin`)

- Dashboard with stats (contacts, suggestions, applications, etc.)
- Site content, hero promises, social links
- Services (technology / digital marketing groups), products, learning programs
- About page, blogs, jobs, applications
- Contact submissions, consultations, client suggestions
- Full CRUD with enable/disable and reorder where applicable

## Quick Start (Local)

```bash
cd Monish_website
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

### Admin Login (local dev)
- URL: **http://127.0.0.1:5000/admin**
- Username: `admin`
- Password: `admin123`

Copy `.env.example` to `.env` to override credentials locally.

## Production Deployment (Render)

### 1. Push to GitHub

```bash
git add .
git commit -m "Deploy Rajaro website"
git push origin main
```

### 2. Deploy with Blueprint (recommended)

Render → **New +** → **Blueprint** → connect repo.  
`render.yaml` creates the web service + PostgreSQL database automatically.

**Live URL format:** `https://rajaro-website.onrender.com` (hyphen, not underscore)

### 3. Required environment variables

Set these in Render if not using Blueprint defaults:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Long random string (Blueprint can auto-generate) |
| `ADMIN_PASSWORD` | Yes | Strong password — **must not** be `admin123` in production |
| `ADMIN_USERNAME` | Optional | Default: `admin` |
| `DATABASE_URL` | Yes | From Render PostgreSQL (auto-linked in Blueprint) |
| `FLASK_ENV` | Yes | `production` |
| `BEHIND_PROXY` | Recommended | `1` — enables correct HTTPS behind Render proxy |

Render sets `RENDER=true` automatically for production security checks.

### 4. Health check

Render uses `GET /health` — returns `{"status":"ok"}`.

### 5. Custom domain

1. Render → Web Service → **Settings** → **Custom Domains**
2. Add your domain and configure DNS (CNAME / A record as shown by Render)
3. Enable **Force HTTPS**

### 6. Uploads on Render

File uploads (blog images, product images, suggestion PDFs, resumes) use the app disk by default.  
On Render free tier this is **ephemeral** — files may be lost on redeploy.  
For persistent uploads, add a [Render Persistent Disk](https://render.com/docs/disks) and set:

```
UPLOAD_FOLDER=/var/data/uploads
```

## Pre-deploy Checklist

- [ ] `ADMIN_PASSWORD` set to a strong value in Render
- [ ] `SECRET_KEY` set (not the dev default)
- [ ] PostgreSQL database linked
- [ ] `/health` returns 200 after deploy
- [ ] Admin login works at `/admin`
- [ ] Test contact, consultation, and suggestion forms
- [ ] Custom domain DNS configured (if applicable)

## Tech Stack

- **Flask** + **Jinja2** — Server-rendered pages
- **HTMX** — Async form submissions
- **Tom Select** — Searchable product/service dropdowns
- **SQLite** (local) / **PostgreSQL** (production)
- **Flask-Login** — Admin authentication
- **Gunicorn** — Production WSGI server
