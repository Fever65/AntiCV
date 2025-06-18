from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('anticv.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    cvs = conn.execute("SELECT * FROM anticv").fetchall()
    conn.close()
    return render_template("index.html", cvs=cvs)

@app.route("/submit_cv", methods=["POST"])
def submit_cv():
    pseudo = request.form["pseudo"]
    titre = request.form["titre"]
    competences = request.form["competences"]
    experiences = request.form["experiences"]
    ambitions = request.form["ambitions"]
    objectif_vie = request.form.get("objectif_vie", "")
    hobbies = request.form.get("hobbies", "")
    animal_totem = request.form.get("animal_totem", "")
    citation = request.form.get("citation", "")
    theme = request.form["theme"]
    type_cv = request.form["type_cv"]
    pfp_ridicule = request.form["pfp_ridicule"]

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO anticv (pseudo, titre, competences, experiences, ambitions,
                            objectif_vie, hobbies, animal_totem, citation,
                            theme, type_cv, pfp_ridicule)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pseudo, titre, competences, experiences, ambitions,
          objectif_vie, hobbies, animal_totem, citation, theme, type_cv, pfp_ridicule))
    conn.commit()
    conn.close()

    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
