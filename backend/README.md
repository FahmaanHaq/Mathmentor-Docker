# Mathmentor Backend API

Django REST Framework backend API for the Mathmentor tutoring platform.

## Features

- User authentication (sign up/login) for Tutors, Students, and Parents
- Session-based authentication
- RESTful API endpoints using Django REST Framework
- Custom User model with role-based access
- PostgreSQL database support
- WebSockets (Channels) for real-time chat and notifications
- CORS configuration for frontend integration

## Quick Setup

See the [root setup guide](../README.md) and [docs/SETUP.md](../docs/SETUP.md) for full setup.

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Edit with your values
python manage.py migrate
python manage.py runserver
```

**Note:** Redis is required for WebSockets. Start `redis-server` before running the app.

## API Endpoints

### Authentication

- `POST /api/auth/tutor/signup/` - Sign up as a tutor
- `POST /api/auth/student/signup/` - Sign up as a student
- `POST /api/auth/parent/signup/` - Sign up as a parent
- `POST /api/auth/login/` - Login (requires verified email)
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Get current user profile (protected)
- `POST /api/auth/verify-email/` - Verify email with 6-digit code
- `POST /api/auth/resend-verification/` - Resend verification code

### Admin

- `GET /admin/` - Django admin interface

## Request/Response Examples

### Sign Up (Tutor)

**Request:**
```json
POST /api/auth/tutor/signup/
{
  "email": "tutor@example.com",
  "password": "Password123",
  "password_confirm": "Password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tutor account created successfully",
  "data": {
    "id": 1,
    "email": "tutor@example.com",
    "role": "TUTOR",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### Login

**Request:**
```json
POST /api/auth/login/
{
  "email": "tutor@example.com",
  "password": "Password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "id": 1,
    "email": "tutor@example.com",
    "role": "TUTOR",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── mathmentor/              # Django project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── accounts/                # Authentication app
    ├── __init__.py
    ├── models.py            # User model
    ├── serializers.py      # DRF serializers
    ├── views.py            # API views
    ├── urls.py             # App URLs
    ├── admin.py
    ├── apps.py
    └── migrations/
```

## Database Setup

Make sure your PostgreSQL database is set up on your VPS:

1. Create database: `CREATE DATABASE mathmentor;`
2. Create user: `CREATE USER your_user WITH PASSWORD 'your_password';`
3. Grant privileges: `GRANT ALL PRIVILEGES ON DATABASE mathmentor TO your_user;`

Update the database connection details in your `.env` file.

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (VPS IP or domain)
- `DB_PORT` - Database port (default: 5432)
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `SESSION_COOKIE_SECURE` - Use secure cookies (True/False)
- `SESSION_COOKIE_NAME` - Session cookie name

### Email Configuration

Railway blocks outbound SMTP. Use **SendGrid** (via `django-anymail`) instead.

#### SendGrid (recommended for Railway)

| Variable | Description |
|---|---|
| `SENDGRID_API_KEY` | Your SendGrid API key (`SG.…`). When set, the backend uses SendGrid automatically — no other email vars needed. |
| `EMAIL_FROM_ADDRESS` | The "From" address. **Must be a verified sender** in your SendGrid account. |
| `EMAIL_TIMEOUT` | Seconds before an email send attempt is abandoned (default: `10`). Prevents signup from hanging. |

Steps:
1. Create a SendGrid account and verify a sender domain or single sender.
2. Generate an API key with **Mail Send** permissions.
3. Add the three variables above to your Railway backend service.
4. Redeploy — signup will now deliver OTP emails via SendGrid.

#### SMTP fallback (local dev / other hosts)

When `SENDGRID_API_KEY` is **not** set the backend falls back to these variables:

| Variable | Default | Description |
|---|---|---|
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` | Set to `django.core.mail.backends.smtp.EmailBackend` for real SMTP. |
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server host |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USE_TLS` | `True` | Enable STARTTLS |
| `EMAIL_HOST_USER` | _(empty)_ | SMTP username |
| `EMAIL_HOST_PASSWORD` | _(empty)_ | SMTP password / app password |
| `EMAIL_FROM_ADDRESS` | `noreply@mathmentor.com` | From address |
| `EMAIL_TIMEOUT` | `10` | Send timeout in seconds |

> **Local dev:** leave `SENDGRID_API_KEY` unset and `EMAIL_BACKEND` at its default (`console`). OTP codes will be printed to the server logs instead of being emailed.

## Development Commands

- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create migration files
- `python manage.py migrate` - Apply migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py shell` - Open Django shell
- `python manage.py collectstatic` - Collect static files (production)

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Set `SECRET_KEY` to a secure random value
3. Update `ALLOWED_HOSTS` with your domain
4. Set `SESSION_COOKIE_SECURE=True` if using HTTPS
5. Configure static files serving
6. Use a production WSGI server (e.g., Gunicorn)
7. Set up reverse proxy (e.g., Nginx)

## Vercel Frontend + Railway Backend: Cross-Site Cookie Setup

When the frontend is hosted on Vercel and the backend on Railway (different domains),
browsers block session cookies by default because `SameSite=Lax` prevents cross-site
cookie sending. The following env vars and settings are required for auth to work:

### Required Railway environment variables

| Variable | Value |
|---|---|
| `DEBUG` | `False` |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |

When `DEBUG=False`, `settings.py` automatically sets both `SESSION_COOKIE_SAMESITE`
and `CSRF_COOKIE_SAMESITE` to `'None'`, which is required for cross-site cookie
transmission over HTTPS. The `Secure` flag is mandatory whenever `SameSite=None`.

### Frontend requirements

Ensure all `fetch` calls in the frontend include `credentials: 'include'` so the
browser sends the session cookie on cross-origin requests. The `apiRequest` helper
in `frontend/src/services/api.js` already does this.

### CORS configuration

`CORS_ALLOW_CREDENTIALS = True` must remain set, and the Vercel origin must be listed
in either `CORS_ALLOWED_ORIGINS` or `CORS_ALLOWED_ORIGIN_REGEXES` in `settings.py`.
