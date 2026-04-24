def test_export_excel(client):
    client.post("/parts", json={
        "name": "Test",
        "price": 10,
        "quantity": 1
    })

    response = client.get("/export/excel")

    assert response.status_code == 200
    assert response.headers["content-type"] == \
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def test_export_pdf(client):
    client.post("/parts", json={
        "name": "Test",
        "price": 10,
        "quantity": 1
    })

    response = client.get("/export/pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"