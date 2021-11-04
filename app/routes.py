from app import db
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from flask import Blueprint, jsonify, make_response, request 


books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")


@books_bp.route("", methods=["POST", "GET"])
def handle_books():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        book = {
            "title" : new_book.title,
            "description" : new_book.description,
            "id" : new_book.id
        }

        return jsonify(book), 201
    
    elif request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()
        
        book = Book.query.all()
        books_response = [book.to_dict() for book in book]
        
        return jsonify(books_response), 200

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify(f"Book {book_id} not found"), 404

    if request.method == "GET":
        book_response = book.to_dict()
        return book_response
    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated.", 200)
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted.", 200)


@authors_bp.route("", methods=["POST", "GET"])
def handle_authors():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_author = Author(
            name=request_body["name"],
            )
        db.session.add(new_author)
        db.session.commit()

        author = {
            "name" : new_author.name,
            "id" : new_author.id
        }

        return jsonify(author), 201
    
    elif request.method == "GET":
        name_query = request.args.get("name")
        if name_query:
            authors = Author.query.filter_by(name=name_query)
        else:
            authors = Author.query.all()
        
        authors_response = []
        for author in authors:
            authors_response.append({
                "id" : author.id,
                "name" : author.name,
            })
        
        return jsonify(authors_response), 200


@authors_bp.route("/<author_id>/books", methods=["GET", "POST"])
def handle_authors_books(author_id):
    author = Author.query.get(id=author_id)
    if author is None:
        return make_response("Author")

    if request.method == "POST":
        request_body = request.get_json()

        new_book = Book(
            title=request_body["title"],
            description=request["description"],
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)

    elif request.method == "GET":
        books_response = []
        for book in author.books:
            books_response.append(
                {
                "id": book.id,
                "title": book.title,
                "description": book.description
                }
            )
        return jsonify(books_response)
        

@genres_bp.route("", methods=["GET","POST"])
def handle_genres():
    if request.method == "GET":
        genres = Genre.query.all()
        genres_response = []
        for genre in genres:
            genres_response.append({
                "id": genre.id,
                "name": genre.name
                })
        return jsonify(genres_response)
    elif request.method == "POST":
        request_body = request.get_json()

        genre = Genre(name=request_body["name"])

        db.session.add(genre)
        db.session.commit()

        return jsonify(f"Genre {genre.name} was successfully created"), 201


@books_bp.route("/<book_id>/assign_genres", methods=["PATCH"])
def assign_genres(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return make_response(f"Book #{book.id} not found", 404)

    request_body = request.get_json()

    for id in request_body["genres"]:
        book.genres.append(Genre.query.get(id))

    db.session.commit()

    return make_response("Genres successfully added", 200)
