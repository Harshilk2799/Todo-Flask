from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy()

# initialize the app with the extension
db.init_app(app)

# Create a Todo Table 
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

# To Generate table
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add a todo
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title = title, desc = desc)
        
        db.session.add(todo)
        db.session.commit()
    
    # show all todos
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)


@app.route("/delete/<int:sno>/", methods=["GET", "POST"])
def delete_todo(sno):
    # Delete specific todo
    todo = Todo.query.filter_by(sno=sno).first()

    db.session.delete(todo)
    db.session.commit()    
    return redirect("/")

@app.route("/update/<int:sno>/", methods=["GET", "POST"])
def update_todo(sno):
    if request.method == "POST":
        # Update Specific todo
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()

        todo.title = title
        todo.desc = desc
        
        db.session.add(todo)
        db.session.commit()
        return redirect("/", 301)

    # Show Specific todo to Update
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    # Default Port = 5000
    app.run(debug=True, port=7002)