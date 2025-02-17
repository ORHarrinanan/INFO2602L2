from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Replace with your DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

app = create_app()

todo_category = db.Table(
    'todo_category',
    db.Column('todo_id', db.Integer, db.ForeignKey('todo.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('last_modified', db.DateTime, default=func.now(), onupdate=func.now())
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    todos = db.relationship('Todo', backref='user', lazy=True, cascade="all, delete-orphan")
    categories = db.relationship('Category', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='scrypt')

    def __repr__(self):
        return f'<User {self.id} {self.username} - {self.email}>'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='todo_list')
    categories = db.relationship('Category', secondary=todo_category, backref='todos')

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

    def toggle(self):
        self.done = not self.done
        db.session.commit()

    def __repr__(self):
        user_name = self.user.username if self.user else "Unknown User"
        return f'<Todo: {self.id} | User: {user_name} | {self.text} | {"done" if self.done else "not done"}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return f'<Category user_id:{self.user_id} - {self.text}>'

                         
                         
                         

                     
                              
                              


                         
                         
                           
                           