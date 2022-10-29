from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

nav_items = [
    {'href': '/', 'title': 'Home', 'active': 'active' },
    {'href': '/notes', 'title': 'Notes', 'active': '' }
]

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000))

@app.route("/") 
def home():
    todo_list = Todo.query.all()
    return render_template("home.html", todo_list=todo_list, nav_items=nav_items)

@app.route("/test") 
def card():
    return render_template("test/check.html")

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# notes

@app.route("/notes/")
def note_index():
    notes = Note.query.all()
    return render_template("notes.html", note_list=notes)

@app.route("/notes/create")
def note_create():
    return render_template("note-create.html")

@app.route("/notes/<int:note_id>/edit", methods=["POST","GET"])
def note_edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        note.title = title
        note.text = text
        db.session.commit()
        return redirect('/notes/'+str(note_id))
    return render_template("note-edit.html", note=note)

@app.route('/notes/<int:note_id>')
def note_view(note_id):
    note = Note.query.filter_by(id=note_id).first()
    return render_template("note.html", note=note)

@app.route("/notes/add", methods=["POST"])
def note_add():
    title = request.form.get("title")
    text = request.form.get("text")
    new_note = Note(title=title, text=text)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("note_index"))

@app.route("/notes/delete/<int:note_id>")
def note_delete(note_id):
    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("note_index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
