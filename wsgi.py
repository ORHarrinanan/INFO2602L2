import click
from models import db, User, Todo, Category
from app import app
from sqlalchemy.exc import IntegrityError

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    bob = User(username='bob', email='bob@mail.com', password='bobpass')
    db.session.add(bob)
    db.session.commit()  # ✅ Make sure Bob is saved before adding Todos

    new_todo = Todo(user_id=bob.id, text='wash car')
    db.session.add(new_todo)
    db.session.commit()

    print(bob)
    print('Database initialized.')

@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    print(user)

@app.cli.command('get-users')
def get_users():
    users = User.query.all()
    for user in users:
        print(user)  # ✅ Print users properly

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    user.email = email
    db.session.commit()
    print(user)

@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("Username or email already taken!")
    else:
        print(new_user)

@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    db.session.delete(user)
    db.session.commit()
    print(f'{username} deleted')

@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    for todo in user.todos:
        print(todo)

@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    new_todo = Todo(user_id=user.id, text=text)  # ✅ Fixed user_id
    db.session.add(new_todo)
    db.session.commit()
    print(f'Task "{text}" added to {username}')

@app.cli.command('toggle-todo')
@click.argument('todo_id', default=1)
@click
