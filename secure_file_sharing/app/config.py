import os

DB_URL = os.environ.get(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/securefiles"
)
JWT_SECRET = os.environ.get("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"
EMAIL_FROM = "no-reply@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "smtp-user"
SMTP_PASS = "smtp-pass"