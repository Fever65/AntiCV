from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt
import html
import os
import secrets

app = Flask(__name__)
app.secret_key = 'TON_SECRET_ULTRA_FORT'  # Remplace par un vrai secret

ALLOWED_COLORS = ["red", "blue", "green", "yellow", "orange", "gray", "purple"]
ALLOWED_IMAGES = [
    "banane.png", "chameau.png", "chat.png", "chien.png",
    "clown.png", "femme1.png", "femme2.png", "pigeon.png"
]

def get_db():
    conn = sqlite3.connect('anticv.db')
    conn.row_factory = sqlite3.Row
    return conn

if not os.path.exists("anticv.db"):
    print("Création de la base de données...")
    os.system("sqlite3 anticv.db < init_db.sql")

@app.route('/')
def index():
    db = get_db()
    profiles = db.execute('SELECT * FROM profiles').fetchall()
    db.close()
    return render_template('index.html', profiles=profiles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db()
        try:
            db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed))
            db.commit()
        except sqlite3.IntegrityError:
            return "Email déjà utilisé", 400
        db.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return "Identifiants invalides", 403

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = html.escape(request.form['name'].strip())
        bio = html.escape(request.form['bio'].strip())
        color = request.form['color'].strip()
        type_cv = request.form['type'].strip()
        image = request.form['image'].strip()

        if color not in ALLOWED_COLORS or type_cv not in ['cv', 'anticv'] or image not in ALLOWED_IMAGES:
            return "Données invalides", 400

        db = get_db()
        db.execute('INSERT INTO profiles (user_id, name, bio, color, type, image) VALUES (?, ?, ?, ?, ?, ?)',
                   (session['user_id'], name, bio, color, type_cv, image))
        db.commit()
        db.close()
        return redirect(url_for('index'))

    return render_template('create.html', colors=ALLOWED_COLORS, images=ALLOWED_IMAGES)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    profile = db.execute('SELECT * FROM profiles WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()

    if not profile:
        db.close()
        return "Non autorisé", 403

    if request.method == 'POST':
        name = html.escape(request.form['name'].strip())
        bio = html.escape(request.form['bio'].strip())
        color = request.form['color'].strip()
        type_cv = request.form['type'].strip()
        image = request.form['image'].strip()

        if color not in ALLOWED_COLORS or type_cv not in ['cv', 'anticv'] or image not in ALLOWED_IMAGES:
            db.close()
            return "Données invalides", 400

        db.execute('UPDATE profiles SET name = ?, bio = ?, color = ?, type = ?, image = ? WHERE id = ?',
                   (name, bio, color, type_cv, image, id))
        db.commit()
        db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('edit.html', profile=profile, colors=ALLOWED_COLORS, images=ALLOWED_IMAGES)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM profiles WHERE user_id = ?', (session['user_id'],))
    db.execute('DELETE FROM users WHERE id = ?', (session['user_id'],))
    db.commit()
    db.close()
    session.clear()
    return redirect(url_for('index'))

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email'].strip()
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user:
            db.close()
            return "Aucun compte avec cet email", 400

        temp_password = secrets.token_hex(8)
        hashed = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())
        db.execute('UPDATE users SET password = ? WHERE email = ?', (hashed, email))
        db.commit()
        db.close()
        return f"Votre nouveau mot de passe temporaire : {temp_password}"

    return render_template('reset.html')

@app.route('/profile/<int:id>')
def profile(id):
    db = get_db()
    profile = db.execute('SELECT * FROM profiles WHERE id = ?', (id,)).fetchone()
    db.close()
    if not profile:
        return "Profil introuvable", 404
    return render_template('profile.html', profile=profile)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
