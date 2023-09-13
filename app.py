from flask import Flask, render_template, request, redirect, url_for, session
import random
import mysql.connector
import pygame

# Initialisieren von pygame
pygame.init()

# Hintergrundmusik laden
background_music = pygame.mixer.Sound('static/Hintergrundmusik.mp3')
background_music.set_volume(0.3)


# Hintergrundmusik abspielen (Endlosschleife)
background_music.play(-1)



app = Flask(__name__)
app.secret_key = "PushinP"

# Verbindung zur MySQL-Datenbank herstellen
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="games"
)
cursor = db.cursor()

# Tabelle erstellen, wenn sie nicht existiert
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        attempts INT NOT NULL
    )
""")
db.commit()

# Startseite 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Zufällige Nummer generieren und in der Session speichern
        session['target_number'] = random.randint(1, 100)
        session['name'] = request.form['name']
        return redirect(url_for('game'))
    return render_template('index.html')

# Spiel-Seite
@app.route('/game', methods=['GET', 'POST'])
def game():
    target_number = session.get('target_number')
    name = session.get('name')
    
    if request.method == 'POST':
        guess = int(request.form['guess'])
        attempts = int(request.form['attempts'])

        if guess == target_number:
            cursor.execute("SELECT attempts FROM scores WHERE name = %s", (name,))
            existing_score = cursor.fetchone()

            if existing_score:
                existing_attempts = existing_score[0]
                if attempts < existing_attempts:
                    cursor.execute("UPDATE scores SET attempts = %s WHERE name = %s", (attempts, name))
                    db.commit()
            else:
                cursor.execute("INSERT INTO scores (name, attempts) VALUES (%s, %s)", (name, attempts))
                db.commit()

            return redirect(url_for('scoreboard'))
        
        if guess < target_number:
            message = 'Höher raten!'
        else:
            message = 'Niedriger raten!'
        
        return render_template('game.html', message=message, name=name, attempts=attempts+1)
    
    return render_template('game.html', message='', name=name, attempts=0)

# Scoreboard-Seite
@app.route('/scoreboard')
def scoreboard():
    cursor.execute("SELECT name, attempts FROM scores ORDER BY attempts")
    scores = cursor.fetchall()
    return render_template('scoreboard.html', scores=scores)


# Optionsseite
@app.route('/options')
def options():
    return render_template('options.html')
 
        

# Route zum Speichern der Einstellungen in Cookies
@app.route('/save_options', methods=['POST'])
def save_options():
    language = request.form.get('language')
    font_size = request.form.get('font-size')
    new_volume = float(request.form.get('volume'))
    background_music.set_volume(new_volume)
    

    # Speichern der Einstellungen in Cookies
    response = app.make_response(redirect(url_for('index')))
    response.set_cookie('language', str(language), max_age=365*24*60*60)
    response.set_cookie('font-size', str(font_size), max_age=365*24*60*60)
    response = app.make_response(render_template('index.html', current_volume=new_volume))
    response.set_cookie('volume', str(new_volume), max_age=365*24*60*60)

    
    return response


if __name__ == '__main__':
    app.run(debug=True)
