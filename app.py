from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content == "":
            return redirect('/')
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        task.date_updated = datetime.utcnow()
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    else:
        return render_template("update.html", task=task)

@app.route("/complete/<int:id>", methods=["GET","POST"])
def complete(id):
    task = Todo.query.get_or_404(id)
    if task.status == 0:
        try:
            task.status = 1
            task.date_updated = datetime.utcnow()
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating the status your task"
    else:
        try:
            task.status = 0
            task.date_updated = datetime.utcnow()
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating the status your task"

@app.route("/clear")
def clear():
    try:
        tasks_to_delete = Todo.query.all()
        for task in tasks_to_delete:
            db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem clearing all tasks"




if __name__ == "__main__":
    app.run(debug=True)
