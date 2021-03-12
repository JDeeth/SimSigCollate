def test_view_server(client):
    """App should provide a list of servers"""
    r = client.get("/servers")
    assert r.status_code == 200
