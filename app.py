from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

DB = 'anticv.db'

def db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT anticv.*, users.pseudo, users.pfp_ridicule, users.theme_couleur
        FROM anticv
        JOIN users ON anticv.user_id = users.id
        WHERE visible = 1
        ORDER BY created_at DESC
    ''')
    cvs = cur.fetchall()
    return render_template('index.html', cvs=cvs)

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

    conn = db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (pseudo, email, password, pfp_ridicule, theme_couleur) VALUES (?, '', '', ?, ?)",
                (pseudo, pfp, couleur))
    user_id = cur.lastrowid
    cur.execute("INSERT INTO anticv (user_id, titre, competences, experiences, ambitions) VALUES (?, ?, ?, ?, ?)",
                (user_id, titre, competences, experiences, ambitions))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

