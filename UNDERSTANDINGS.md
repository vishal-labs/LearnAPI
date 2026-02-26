### Here are my new findings while trying to build a simple JWT OAuth application using FastAPI

1. When we try to modularise the code, we tend to seperate the routings, main logic, dbConnections..
2. When we have different functions for different utilities and say Function B depends on A, we can use
   `from fastapi import Depends` and then pass the function call in the depends call like `db: Session = Depends(get_db)`
   - Directly calling `get_db()` or similar works but bypasses FastAPI's caching and lifecycle management: it creates sessions per call (not per request), skips automatic commit/rollback/yield cleanup, and complicates testing/overriding
   - Dependencies provide automatic resolution, sub-dependency support, and one session per request
3. Creating the token for any user is very interesting, this is what i understood:
   - When the user posts to the backend with their username and password, first the backend validates the JSON signature.
   - Then, A DB query is done to check if the user actually exists and if the user exists, a token is generated
   - To generate a token,
     - First we _Embed_ the expiry time of the token, Say 15 minutes of 20 minutes(we use the timedelta function)
       `expire = datetime.now(timezone.utc) + timedelta(minutes=expireMinutes)`
     - If embedding is done properly, the new payload will have username and the `exp` key.
     - This entire payload is encoded using JWT by passing the payload, Key(when we generated separately)
     - Finally, the encoded payload is a string which is returned from the endpoint in the format
       `{"access_token" : token, "token_type": "bearer"}`
4. Now that we have, the token we can use different errors from the `JWT` to check if the token is expired or not.
   `jwt.ExpiredSignatureError or jwt.InvalidTokenError`
5. We can use the above Errors in a function and use that Function as Dependent for any other functions for modularity
6. Understood how SQLALCHEMY creates a DB connection(the 3 step process: Engine -> sessionMaker -> Session)
7. I was using the wrong user in the database and hence the queries were not being executed properly, but now i modified it.
8. Was able to write DB queries for login, siginup and also validate the user. This is quite simple, for the signup endpoint, just get the
   User details from the user variable, and also, get the DB dependency. Once that is done, execute the SQL query to check if the user is already created or not, and if not, then do an SQL insertion to create the user.
9. In Login, check if the username and password match using an SQL query, if both of them match, call the tokengenerator function to create a token
   for the user and return the bearer token
10. I also understood, how to get the bearer token for any other Endpoints `Use HTTPBearer and HTTPAuthorizationCredentials from the fastapi.security`
    With this, i can get the bearer token, validate the lifespan of it, and if the token is expired, do not proceed further.
11. As a general Practice, use OAuth2_scheme to check if the token is actually being generated from the endpoint that we intended from.
12. Only use endpoints by starting them with `/`
13. While using the SQLALchemy ORM for db queries, all of the queries return the Object not the value that we are expecting directly, so check how to extract the message directly.

14. Using Alembic to create a database migration/modification is a little tricky, the basic ORM code that we right
   might sometimes break the alembic migration process Ex. `default vs server_default` (i might only know this)
15. When calling a helper function inside a main function, if the helper function requires something as a parameter,
   and the main function can provide that, than pass that parameter directly to the helper function, instead of using Depends. Should learn more about this. 