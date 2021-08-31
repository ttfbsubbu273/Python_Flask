from flask import Flask, app, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    complete = db.Column(db.Boolean)

@app.route("/")
def homepage():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=['GET','POST'])
def add():
    titlename = request.form.get('titlehead')
    new_todo = Todo(title=titlename, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("homepage"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo_update = Todo.query.filter_by(id=todo_id).first()
    todo_update.complete = not todo_update.complete
    db.session.commit()
    return redirect(url_for("homepage"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_detete = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_detete)
    db.session.commit()
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) 