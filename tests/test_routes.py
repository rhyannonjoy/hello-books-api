def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_create_a_book(client):
    # act
    response = client.post("/books", json = {
        "title" : "The Never Ending Story",
        "description" : "The horse dies"
    })
    response_body = response.get_json()
    
    # assert
    assert response.status_code == 201
    assert response_body == {
        "id" : 1,
        "title" : "The Never Ending Story",
        "description": "The horse dies"
    }

    