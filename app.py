from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(60), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

# cRud
@app.route("/")
def index():
    tasks = Tasks.query.all()   
    return render_template("index.html", tasks=tasks)

# Crud
@app.route("/create", methods=["POST"])
def create_task():
    description = request.form["description"]
    value = True if request.form.get("active") == "1" else False
    active = value

    # Valida se registro já existe
    task_exist = Tasks.query.filter_by(description = description).first()

    if task_exist:
        return "Erro: Tarefa já existe!!!", 400

    new_task = Tasks(description = description, active = active)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

# crUd
@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        task.description = request.form["description"]
        db.session.commit()
    return redirect("/")

#cruD
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5153)