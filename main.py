from flask import *
import sqlite3
import random
import string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
"""app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////link.db"""

def generate_random_string():
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(5))
    print(rand_string)
    return rand_string

@app.route('/', methods=['GET', 'POST'])
def programs():
    if request.method == 'POST':
        link = request.form['link']
        try:
            resault = generate_random_string()
            print(resault)
            db = sqlite3.connect('link.db')
            cur = db.cursor()
            cur.execute(f"INSERT INTO osn(start_link, res_link) VALUES ('{link}', '{resault}')").fetchall()
            db.commit()
            cur.close()
            return (f'{str(request.host)}/{resault}')
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
    return render_template('home.html')

@app.route("/<smth>", methods=['GET', 'POST'])
def test(smth):
    try:
        db = sqlite3.connect('link.db')
        cur = db.cursor()
        print(smth)
        a = cur.execute(f"SELECT start_link FROM osn WHERE res_link='{smth}'").fetchone()
        a = str(a)[2:-3]
        return redirect(f"https://{a}")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    return ('ошибка')

if __name__ == '__main__':
    app.run(debug=True)