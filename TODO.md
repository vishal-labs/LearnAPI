# TODO

## Completed

- [x] ~~Create an admin route to return all users~~ (`GET /admin/users`)
- [x] ~~Hash passwords~~ — `passlib` + `bcrypt` now hash on signup and verify on login
- [x] ~~Extract user identity from JWT~~ — Endpoints use JWT-decoded identity
- [x] ~~Fix `return HTTPException` → `raise HTTPException`~~
- [x] ~~Add balance check to withdrawal~~ — Guard added in `/user/withdrawal`
- [x] ~~Validate transaction amounts~~ — `Field(gt=0)` on `transactionAmount`
- [x] ~~Clean up `transactionprocessing.py`~~ — Removed duplicate file
- [x] ~~Create more tables / learn ORM relationships~~
- [x] ~~Add DB-level balance constraint~~ — `CHECK(accountbalance >= 0)` on `useraccountbalance`

---

## Foundational

- [ ] Implement a Forgot Password feature

---

## Security & Authentication

- [ ] **Implement refresh tokens** — Token expires in 4 minutes. Add a `/auth/refresh` endpoint that uses a longer-lived refresh token to issue new short-lived access tokens.

---

## Error Handling & Correctness

- [ ] **Global exception handling** — Write a FastAPI `@app.exception_handler()` to catch common errors (e.g., `jwt.ExpiredSignatureError`) app-wide instead of per-endpoint try/except blocks.

---

## API Design

- [ ] **Use GET for read-only endpoints** — `/user/balance` and `/user/transactions` only read data. Once user identity comes from JWT, convert them to GET (no request body needed).

---

## Testing

- [ ] **Write unit/integration tests** — Currently zero tests. Use `pytest` + FastAPI `TestClient`. Start with auth flows, then transactions, then validation.

---

## Developer Experience

- [ ] **Use Pydantic `BaseSettings`** — Replace scattered `os.getenv()` calls with a `BaseSettings` class that auto-loads `.env`, validates types, and provides a clean singleton config object.
