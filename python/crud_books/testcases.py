import requests

BASE_URL = "http://localhost:8000"


def test_create_book():
    new_book = {
        "title": "1984",
        "author": "George Orwell",
        "published_year": 1949
    }
    response = requests.post(f"{BASE_URL}/books", json=new_book)
    print(f"Create book response status code: {response.status_code}")
    print(f"Create book response content: {response.text}")
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}"
    )
    created_book = response.json()
    assert "id" in created_book
    assert created_book["title"] == new_book["title"]
    assert created_book["author"] == new_book["author"]
    assert created_book["published_year"] == new_book["published_year"]
    return created_book["id"]


def test_read_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) > 0


def test_read_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    book = response.json()
    assert book["id"] == book_id


def test_update_book(book_id):
    updated_book = {
        "title": "1984 (Updated)",
        "author": "George Orwell",
        "published_year": 1950,
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=updated_book)
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == book_id
    assert updated["title"] == updated_book["title"]
    assert updated["published_year"] == updated_book["published_year"]


def test_delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    # Verify the book is deleted
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    assert response.status_code == 404


def run_tests():
    print("Running API tests...")

    # Test CREATE
    print("Testing CREATE...")
    book_id = test_create_book()
    print("CREATE test passed.")

    # Test READ (all books)
    print("Testing READ (all books)...")
    test_read_books()
    print("READ (all books) test passed.")

    # Test READ (single book)
    print("Testing READ (single book)...")
    test_read_book(book_id)
    print("READ (single book) test passed.")

    # Test UPDATE
    print("Testing UPDATE...")
    test_update_book(book_id)
    print("UPDATE test passed.")

    # Test DELETE
    print("Testing DELETE...")
    test_delete_book(book_id)
    print("DELETE test passed.")

    print("All tests passed successfully!")


if __name__ == "__main__":
    run_tests()
