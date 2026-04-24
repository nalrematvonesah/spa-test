def test_create_part(client):
    response = client.post("/parts", json={
        "name": "Engine",
        "price": 100,
        "quantity": 2
    })

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Engine"
    assert data["price"] == 100


def test_tree_structure(client):
    root = client.post("/parts", json={
        "name": "Car",
        "price": 0,
        "quantity": 1
    }).json()

    client.post("/parts", json={
        "name": "Wheel",
        "price": 50,
        "quantity": 4,
        "parent_id": root["id"]
    })

    response = client.get(f"/parts/{root['id']}")
    data = response.json()

    assert len(data["children"]) == 1


def test_invalid_quantity(client):
    response = client.post("/parts", json={
        "name": "Test",
        "price": 10,
        "quantity": 0
    })

    assert response.status_code == 400