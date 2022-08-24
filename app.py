from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    items = db.relationship('Item', backref='todos')

    def __repr__(self):
        return f"<Todo - %s>" % self.description


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), nullable=False)

    def __repr__(self):
        return f"<Item - %s>" % self.name


db.create_all()


@app.route('/create_todo')
def create_todo():
    todo = Todo(description="Hello, world!")
    db.session.add(todo)
    db.session.commit()

    return redirect('/')


@app.route('/delete/<item>')
def delete_item(item):
    todo = Todo.query.get(item)
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')


@app.route('/update/<item>')
def update_item(item):

    todo = Todo.query.get(item)
    todo.description = "je suis un Millionnaire"
    db.session.commit()

    return redirect('/')


@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.all())


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0")
