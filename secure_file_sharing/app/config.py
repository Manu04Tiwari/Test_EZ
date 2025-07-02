import os

MONGODB_URL = os.environ.get(
    "MONGODB_URL",
    "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
DB_NAME = os.environ.get("MONGODB_DB", "<dbname>")
JWT_SECRET = os.environ.get("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"
EMAIL_FROM = "no-reply@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "smtp-user"
SMTP_PASS = "smtp-pass"