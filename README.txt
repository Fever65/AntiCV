# AntiCV Project

## 🐍 Backend Python (Flask)
### Installation :
1. Assure-toi d'avoir Python installé.
2. Ouvre un terminal dans ce dossier.
3. Installe Flask :
```bash
pip install flask flask-cors
```

### Lancement :
```bash
python app.py
```

## 💠 Front-end FlutterFlow
Crée une app FlutterFlow qui appelle les endpoints suivants :
- POST `/api/create_user`
- POST `/api/create_cv`
- GET `/api/anticvs`
- POST `/api/vote`

Chaque AntiCV contient : titre, compétences, expériences, ambitions, thème, image.

## 🚀 Déploiement
Déploie `app.py` et `anticv.db` sur Render ou Railway.

1. Va sur https://render.com/
2. Crée un nouveau service web
3. Upload ce dossier ou connecte ton repo GitHub
4. Choisis le `build command` : `pip install flask flask-cors`
5. Start command : `python app.py`

