# https://www.youtube.com/watch?v=Z1RJmh_OqeA

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # referencing this file (app.py)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # tells app where database is located, 3*/ is relative path, 4*/ is absolute
db = SQLAlchemy(app)

# create model whenever new entry is created
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # references id of each entry
    content = db.Column(db.String(200), nullable=False) # max 200 characters, nullable=False means user can't create empty task
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) # prevents 404, methods lets us send and receive data
def index():
    if request.method == 'POST':
        # put data in database
        task_content = request.form['content'] # create task using input in form
        new_task = Todo(content=task_content) # 

        try: # try committing to database and redirect back to index page
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # looks at all database contents in order they were created and returns all of them
        return render_template('index.html', tasks=tasks) # render_template will automatically look in templates folder 

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)