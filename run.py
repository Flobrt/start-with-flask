from flask import Flask, render_template, request
import mariadb
import pandas as pd
import numpy as np
from PIL import Image
import joblib
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Page2')
def Page2():
    return render_template('Page2.html')


@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        sexe = request.form['gender']
        pseudo = request.form['pseudo']
        return render_template('resultat_formulaire.html', nom=nom, prenom=prenom, sexe=sexe, pseudo=pseudo)
    
    return render_template('formulaire.html')


@app.route('/utilisateur', methods=['GET', 'POST'])
def utilisateur():

    config = {
            'user': 'florian_docker',
            'password': 'florian038',
            'host': '127.0.0.1',
            'port': 3306
        }

    # Connexion à la base de données
    conn = mariadb.connect(**config)
    # Récupération d'un curseur
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test")
    cursor.execute("USE test")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            prenom VARCHAR(100),
            pseudo VARCHAR(100) UNIQUE,
            sexe VARCHAR(10))
    ''')

    if request.method == 'POST':
        try : 
            insert_query = """
            INSERT INTO user (nom, prenom, pseudo, sexe)
            VALUES (%s, %s, %s, %s)
            """

            username = request.form['pseudo']
            nom = request.form['nom']
            prenom = request.form['prenom']
            sexe = request.form['gender']
            
            data = (nom, prenom, username, sexe)
            cursor.execute(insert_query, data)
            conn.commit()
            conn.close()
            return render_template('resultat_utilisateur.html', nom=nom, prenom=prenom, sexe=sexe, pseudo=username)
    
        except mariadb.IntegrityError as e:
            return render_template('utilisateur.html', error='Ce pseudo existe déjà.')
    
    requete_all_user = """
        SELECT * FROM user
    """
    cursor.execute(requete_all_user)
    users = cursor.fetchall()
    conn.close()

    return render_template('utilisateur.html', users=users)

@app.route('/dataframe', methods=['GET', 'POST'])
def dataframe():
    if request.method == 'POST':
        csv = request.files['fichier']
        df = pd.read_csv(csv)
        result = df.describe()
        return render_template('resultat_dataframe.html', result=result)
    
    return render_template('dataframe.html')

# Utilisation d'un modele de machine learning pour determiner le chiffre sur une image
@app.route('/machine_learning', methods=['GET', 'POST'])
def machine_learning():
    
    if request.method == 'POST':
        path = 'static/model.pkl'  # Chemin complet du modèle sauvegardé
        loaded_model = joblib.load(path)

        image_file = request.files['fichier']
        new_image = Image.open(image_file)
        new_image = new_image.convert('L')
        new_image = new_image.point(lambda x: 255 - x)
        new_image = new_image.resize((28, 28))
        new_image_array = np.array(new_image)
        new_image_array = new_image_array.flatten()


        prediction = loaded_model.predict(new_image_array.reshape(1, -1))   
        predicted_label = prediction[0]
        print(predicted_label)  # Affichage du chiffre prédit dans le terminal
        return render_template('resultat_machine_learning.html', predicted_label=predicted_label, prediction=prediction)
    
    return render_template('machine_learning.html')

@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
    if request.method == 'POST':
        path = 'static/model.joblib'  # Chemin complet du modèle sauvegardé    
        loaded_model = joblib.load(path)

        image_data = request.form['image']
        image_data = image_data.split(',')[1]
        image_byte = base64.b64decode(image_data)
        new_image = Image.open(image_byte)
        new_image = new_image.convert('L')
        new_image = new_image.point(lambda x: 255 - x)
        new_image = new_image.resize((28, 28))
        new_image_array = np.array(new_image)
        new_image_array = new_image_array.flatten()


        prediction = loaded_model.predict(new_image_array.reshape(1, -1))   
        predicted_label = prediction[0]
        print(predicted_label)

        return render_template('resultat_canvas.html', predicted_label=predicted_label, prediction=prediction)
    return render_template('canva.html')


if __name__ == '__main__':
    app.run(debug=True)