from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

class DeletedTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    deleted_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get(id)

    if todo_to_delete:
        # Create a deleted todo record
        deleted_todo = DeletedTodo(content=todo_to_delete.content)
        db.session.add(deleted_todo)

        # Delete the todo from the main table
        db.session.delete(todo_to_delete)

        db.session.commit()

    return redirect(url_for('index'))

@app.route('/history')
def history():
    deleted_todos = DeletedTodo.query.all()
    return render_template('history.html', deleted_todos=deleted_todos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
