def fake_storage_export(**updates):
    storage_res = {
        "sessions": [
            {
                "ip": "127.0.0.1",
                "sid": "1",
                "tid": "1",
            }
        ],
        "tid": "1",
        "volume": "fake"
    }

    if updates:
        storage_res.update(updates)

    return storage_res
