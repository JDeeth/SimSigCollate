def test_empty_server_list(client):
    """
    GIVEN a fresh database
    WHEN the client requests the server list
    THEN the client should receive an empty list
    """
    response = client.get("/servers/")
    assert response.status_code == 200
    assert response.json == []


def test_add_server(client):
    """
    GIVEN any state
    WHEN the client adds a server with complete info
    THEN the server is added
    """
    response = client.post(
        "/servers/", data=dict(name="Sleve McDichael", uri_host="localhost")
    )
    assert response.status_code == 201
    assert response.headers["location"] == "http://localhost/servers/1"
    assert response.json == {"message": "created"}
    response = client.get("/servers/")
    assert response.status_code == 200
    assert b"Sleve McDichael" in response.data


def test_server_requires_host(client):
    """
    GIVEN any state
    WHEN the client adds a server without a hostname
    THEN the server is not added with a suitable error code / message
    """
    response = client.post("/servers/", data={})
    assert response.status_code == 400
    assert b"uri_host" in response.data
    assert b"Missing data for required field." in response.data


def test_server_authority_is_unique(client):
    """
    GIVEN at least one server already recorded
    WHEN the client adds a server with a duplicate URI authority
    THEN the server is not added with a suitable error code / message
    """
    uri = {"uri_host": "simsig.co.uk", "uri_port": 51515}
    assert client.post("/servers/", data=uri).status_code == 201
    uri["uri_port"] = 51517
    assert client.post("/servers/", data=uri).status_code == 201
    duplicate_resp = client.post("/servers/", data=uri)
    assert duplicate_resp.status_code == 400
    assert b"uri not unique" in duplicate_resp.data
