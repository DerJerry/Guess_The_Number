from flask import Flask, render_template, request, redirect, url_for
import random
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="game"
)
cursor = db.cursor()


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
        target_number = random.randint(1, 100)
        name = request.form['name']
        return redirect(url_for('game', target_number=target_number, name=name))
    return render_template('index.html')

# Spiel-Seite
@app.route('/game/<int:target_number>/<name>', methods=['GET', 'POST'])
def game(target_number, name):
    if request.method == 'POST':
        guess = int(request.form['guess'])
        attempts = int(request.form['attempts'])

        if guess == target_number:
            # Überprüfen, ob der Spieler bereits einen Eintrag in der Datenbank hat
            cursor.execute("SELECT attempts FROM scores WHERE name = %s", (name,))
            existing_score = cursor.fetchone()

            if existing_score:
                existing_attempts = existing_score[0]
                if attempts < existing_attempts:
                    # Besseren Score aktualisieren
                    cursor.execute("UPDATE scores SET attempts = %s WHERE name = %s", (attempts, name))
                    db.commit()
            else:
                # Eintrag in die Datenbank einfügen
                cursor.execute("INSERT INTO scores (name, attempts) VALUES (%s, %s)", (name, attempts))
                db.commit()

            return redirect(url_for('scoreboard'))
        
        if guess < target_number:
            message = 'Höher raten!'
        else:
            message = 'Niedriger raten!'
        
        return render_template('game.html', target_number=target_number, message=message, name=name, attempts=attempts+1)
    
    return render_template('game.html', target_number=target_number, message='', name=name, attempts=0)

        


# Scoreboard-Seite
@app.route('/scoreboard')
def scoreboard():
    cursor.execute("SELECT name, attempts FROM scores ORDER BY attempts")
    scores = cursor.fetchall()
    return render_template('scoreboard.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
