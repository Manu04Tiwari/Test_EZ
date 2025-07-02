# Secure File Sharing System

A FastAPI-based backend for secure file sharing, featuring:
- User authentication (JWT)
- Role-based access (client, ops)
- MongoDB Atlas integration
- Secure file uploads (.pptx, .xlsx, .docx)
- Email verification support

## Features

- Sign up with email and password
- User roles: client, ops (operations)
- JWT-based authentication
- MongoDB as the backend database (Atlas or local)
- File upload and download endpoints
- File type validation for uploads
- Email verification (requires SMTP setup)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Set these in your terminal before running the app (replace with your actual values):

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/securefiles?retryWrites=true&w=majority"
export MONGODB_DB="securefiles"
export JWT_SECRET="your_jwt_secret"
```

On Windows (Command Prompt):

```cmd
set MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/securefiles?retryWrites=true&w=majority"
set MONGODB_DB=securefiles
set JWT_SECRET=your_jwt_secret
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Usage

- Use `/signup` to create a new user.
- Log in to receive a JWT token.
- Use the token with the "Authorize" button in the API docs for protected endpoints.
- Upload files using `/ops/upload` (role: ops).

## Configuration

All sensitive data and credentials are configured via environment variables:

- `MONGODB_URL` - MongoDB connection string
- `MONGODB_DB` - Database name
- `JWT_SECRET` - Secret key for JWT
- SMTP settings for email (in `app/config.py`)

## Folder Structure

```
secure_file_sharing/
    app/
        main.py
        database.py
        schema.py
        auth.py
        file_utils.py
        email_utils.py
        config.py
        routers/
            client.py
            ops.py
    uploads/       # Files uploaded are stored here
```

## License

MIT License

---

**Enjoy your secure file sharing system!**