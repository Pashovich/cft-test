import time
import pytest
transactions = [
    {
        "data": {
            "cur" : "RUB",
            "country" : "RUS",
            "amount" : 1,
            "date" : int(time.time())
        },
        "response" : 200
    },
    {
        "data": {
            "cur" : "RUB",
            "country" : "AUS",
            "amount" : 1,
            "date" : int(time.time())
        },
        "response" : 404
    }
]

@pytest.fixture
async def created_user(api):
    api_client = api[0]
    app = api[1]
    data = {
        "cur" : "RUB",
        "country" : "RUS",
        "limit" : 90
    }
    resp = await api_client.post(
        app.router['limit_post'].url_for(), json = data
    )
    data = await resp.json()
    client = data['client_id']
    return client



@pytest.mark.parametrize('transaction', transactions)
async def test_make_transaction(api,created_user, transaction):
    api_client = api[0]
    app = api[1]
    transaction['data']['client_id'] = created_user
    resp = await api_client.post(
        app.router['transaction_post'].url_for(), json = transaction['data']
    )

    assert resp.status == transaction['response']

