from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Model class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # References the ID of each entry
    content = db.Column(db.String(200), nullable=False) # The content of each entry (Max of 200 characters string)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # Creates a date and time for each entry

    # Return an string for each entry created along with its ID
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except:
            return "Problem: couldn't add the task!"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/')
    except:
        return "Problem: couldn't delete the task!"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()

            return redirect('/')
        except:
            return "Problem: couldn't update the task"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
