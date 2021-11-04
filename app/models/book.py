from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="books")
    genres = db.relationship("Genre", secondary="books_genres", backref="books")

    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"

    def to_dict(self):
        genres = []
        for genre in self.genres:
            genres.append(genre.name)

        if self.author:
            author = self.author.name
        else:
            author = None
        
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genres": genres,
            "author": author,
        }