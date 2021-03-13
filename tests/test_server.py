def add_server(client, **kwargs):
    """Convenience function for creating a server"""
    if "uri_host" not in kwargs:
        kwargs["uri_host"] = "localhost"
    return client.post("/servers/", data=kwargs)


def test_empty_server_list(client):
    """
    GIVEN a fresh database
    WHEN the client requests the server list
    THEN the client should receive an empty list
    """
    response = client.get("/servers/")
    assert response.status_code == 200
    assert response.json == []

    response = client.get("/servers/1")
    assert response.status_code == 404
    assert response.json["error"] == "not found"


def test_add_server(client):
    """
    GIVEN any state
    WHEN the client adds a server with complete info
    THEN the server is added
    """
    response = client.post(
        "/servers/",
        data={
            "name": "Sleve McDichael",
            "uri_host": "localhost",
        },
    )
    assert response.status_code == 201
    assert response.json["message"] == "created"
    location = response.headers["location"]
    assert location[-10:] == "/servers/1"

    response = client.get(location)
    assert response.status_code == 200
    assert response.json["uri_host"] == "localhost"


def test_populated_server_list(client):
    """
    GIVEN servers have been listed
    WHEN asking for the list
    THEN the client gets the list
    """
    add_server(client, uri_host="localhost")
    add_server(client, uri_host="192.168.0.30")
    response = client.get("/servers/")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_server_requires_host(client):
    """
    GIVEN any state
    WHEN the client adds a server without a hostname
    THEN the server is not added with a suitable error code / message
    """
    response = client.post("/servers/", data={})
    assert response.status_code == 400
    assert "Missing data for required field." in response.json["uri_host"]


def test_server_authority_is_unique(client):
    """
    GIVEN at least one server already recorded
    WHEN the client adds a server with a duplicate URI authority
    THEN the server is not added with a suitable error code / message
    """
    # add first server = OK
    response = add_server(client, uri_host="simsig.co.uk", uri_port=51515)
    assert response.status_code == 201

    # add server at same host, different port = OK
    response = add_server(client, uri_host="simsig.co.uk", uri_port=51517)
    assert response.status_code == 201

    # add server at different host, different port = OK
    response = add_server(client, uri_host="localhost", uri_port=51517)
    assert response.status_code == 201

    # add duplicate server = error
    response = add_server(client, uri_host="simsig.co.uk", uri_port=51517)
    assert response.status_code == 400
    assert response.json["message"] == "uri already added"


def test_delete_server(client):
    """
    GIVEN a server is recorded
    WHEN the client removes the server
    THEN the server is removed
    """

    response = add_server(client)
    assert response.status_code == 201
    location = response.headers["location"]

    response = client.delete(location)
    assert response.status_code == 200
    assert response.json["message"] == "deleted"

    # deleting a server that's not listed should fail
    assert client.delete(location).status_code == 404

    # adding a new server should use a new location
    response = add_server(client)
    assert response.headers["location"] != location
