# TODO

## Foundational (Original Goals)

- [ ] Create more tables to learn ORM queries and relationship management
- [ ] Get more comfortable with Pydantic and SQLModels for API parameters and DB queries
- [ ] Implement a Forgot Password feature
- [ ] ~~Create an admin route to return all users~~ ✅ Done (`GET /admin/users`)

---

## Security & Authentication

- [ ] **Hash passwords** — `passlib` + `bcrypt` are already imported but signup still saves plain-text. Actually hash before storing and verify during login.
- [ ] **Extract user identity from JWT** — Endpoints like `/user/balance` trust the email in the request body. Instead, decode the JWT to get the logged-in user's email — prevents users from accessing other accounts.
- [ ] **Implement refresh tokens** — Token expires in 4 minutes. Add a `/auth/refresh` endpoint that uses a longer-lived refresh token to issue new short-lived access tokens.

---

## Error Handling & Correctness

- [ ] **Fix `return HTTPException` → `raise HTTPException`** — Several error paths in `accountholder.py` return the exception instead of raising it, sending a `200 OK` with a serialized error object.
- [ ] **Add balance check to withdrawal** — `/user/withdrawal` subtracts without verifying sufficient funds. Match the guard already in `/user/transfer`.
- [ ] **Validate transaction amounts** — Add `Field(gt=0)` on `transactionAmount` in Pydantic models to reject negative/zero values.
- [ ] **Global exception handling** — Write a FastAPI `@app.exception_handler()` to catch common errors (e.g., `jwt.ExpiredSignatureError`) app-wide instead of per-endpoint try/except blocks.

---

## Database & Architecture

- [ ] **Clean up `transactionprocessing.py`** — Near-duplicate of `accountholder.py` and not mounted in `main.py`. Delete it or give it a distinct responsibility.
- [ ] **Add DB-level balance constraint** — Add a `CHECK(accountbalance >= 0)` constraint on `useraccountbalance` as a database-level safety net.

---

## API Design

- [ ] **Use GET for read-only endpoints** — `/user/balance` and `/user/transactions` only read data. Once user identity comes from JWT, convert them to GET (no request body needed).
- [ ] **Add pagination to transaction history** — `/user/transactions` returns everything at once. Add `limit`/`offset` query parameters.

---

## Testing

- [ ] **Write unit/integration tests** — Currently zero tests. Use `pytest` + FastAPI `TestClient`. Start with auth flows, then transactions, then validation.

---

## Developer Experience

- [ ] **Use Pydantic `BaseSettings`** — Replace scattered `os.getenv()` calls with a `BaseSettings` class that auto-loads `.env`, validates types, and provides a clean singleton config object.
