def test_deposit_and_balance(client, random_email):
    # Setup: Create user and login
    client.post(
        "/auth/signup",
        json={"username": "txuser", "email": random_email, "password": "password123"}
    )
    login_resp = client.post(
        "/auth/login",
        json={"email": random_email, "password": "password123"}
    )
    token = login_resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Deposit
    deposit_resp = client.post(
        "/user/deposit",
        json={
            "fromUserEmail": random_email, # Not used in deposit but required by model
            "toUserEmail": random_email,
            "transactionAmount": 500
        },
        headers=headers
    )
    assert deposit_resp.status_code == 200
    assert deposit_resp.json()["DepositedAmt"] == 500

    # 2. Balance
    balance_resp = client.get(
        "/user/balance",
        headers=headers
    )
    assert balance_resp.status_code == 200
    assert balance_resp.json()["accountBalance"] == 500

    # 3. Withdraw
    withdraw_resp = client.post(
        "/user/withdrawal",
        json={
            "fromUserEmail": random_email,
            "toUserEmail": random_email,
            "transactionAmount": 200
        },
        headers=headers
    )
    assert withdraw_resp.status_code == 200
    
    # 4. Check Balance again
    balance_resp2 = client.get(
        "/user/balance",
        headers=headers
    )
    assert balance_resp2.status_code == 200
    assert balance_resp2.json()["accountBalance"] == 300

    # 5. Get transactions
    tx_resp = client.get(
        "/user/transactions",
        headers=headers
    )
    assert tx_resp.status_code == 200
    txs = tx_resp.json()
    assert len(txs) == 2  # One deposit, one withdrawal
