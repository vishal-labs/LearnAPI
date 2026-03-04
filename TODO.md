1. Create more tables to learn more ORM queries and relationship management
2. Get more comfortable with using Pydantic and SQLModels for API parameters and DB queries/construction.
3. Implement Forgot password feature
4. Create an admin route to return all of the users in the database.(should create auth for admin, for that should change the usertableschema)

5.

## Incremental Learning Tasks (Added!)

### Security & Authentication

5. **Hash Passwords (CRITICAL)**: Replace storing plain-text passwords in the DB by hashing them before saving (look into `passlib` and `bcrypt`). Write a utility function to verify hashes during login.
6. **Refresh Tokens**: Your token expires in 1 minute. Implement a `/refresh` endpoint that takes a longer-lived "Refresh Token" to generate a new short-lived "Access Token", so the user doesn't have to keep typing their password.

### Database & Architecture

9. **Global Exception Handling**: Instead of individually catching exceptions and raising `HTTPException(403)` everywhere, learn how to write a global FastAPI `@app.exception_handler()` to catch errors (like `jwt.ExpiredSignatureError`) application-wide and return formatted JSON error responses.

### Web Application Necessities

11. **Environment Variables via Pydantic (`BaseSettings`)**: You are currently using `os.getenv()`. Pydantic has a `BaseSettings` feature that automatically loads `.env` files, validates the types (e.g., ensuring port numbers are `int`), and provides them as a singleton object. It is much cleaner!
