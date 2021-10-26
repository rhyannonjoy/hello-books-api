from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request 


books_bp = Blueprint("books", __name__, url_prefix="/books")

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

        return f"Book {new_book.title} created", 201
    
    elif request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()
        
        books_response = []
        for book in books:
            books_response.append({
                "id" : book.id,
                "title" : book.title,
                "description" : book.description
            })
        
        return jsonify(books_response), 200

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify(f"Book {book_id} not found"), 404

    if request.method == "GET":
        return {
            "id" : book.id,
            "title" : book.title,
            "description" : book.description
        }
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