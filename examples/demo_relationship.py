import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from safrs import SAFRSBase, SafrsApi

db = SQLAlchemy()

# Example sqla database objects
class User(SAFRSBase, db.Model):
    """
    description: User description
    """
    __tablename__ = "Users"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    email = db.Column(db.String, default="")
    books = db.relationship("Book", back_populates="user", lazy="dynamic")

class Book(SAFRSBase, db.Model):
    """
    description: Book description
    """
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    user_id = db.Column(db.String, db.ForeignKey("Users.id"))
    user = db.relationship("User", back_populates="books")

# Create the api endpoints
def create_api(app, host="localhost", port=5000, api_prefix=""):
    api = SafrsApi(app, host=host, port=port, prefix=api_prefix)
    api.expose_object(User)
    api.expose_object(Book)
    print(f"Created API: http://{host}:{port}/{api_prefix}")

def create_app(config_filename=None, host="localhost", port=5000):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI=f"sqlite://")
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_api(app, host, port)
        # Populate the db with users and a books and add the book to the user.books relationship
        for i in range(200):
            user = User(name=f"user{i}", email=f"email{i}@email.com")
            book = Book(name=f"test book {i}")
            user.books.append(book)
            
    return app

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    app = create_app(host=host, port=port)
    app.run(host=host, port=port)