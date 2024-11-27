
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, 
                  weight REAL, 
                  height REAL, 
                  bmi REAL, 
                  category TEXT)''')
    conn.commit()
    conn.close()

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        bmi = calculate_bmi(weight, height)
        category = interpret_bmi(bmi)
        
        # Save to database
        conn = sqlite3.connect('bmi_records.db')
        c = conn.cursor()
        c.execute('INSERT INTO records (name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)',
                  (name, weight, height, round(bmi, 2), category))
        conn.commit()
        conn.close()
        
        return render_template('result.html', name=name, bmi=round(bmi, 2), category=category)
    return render_template('index.html')

@app.route('/history')
def history():
    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records ORDER BY id DESC')
    records = c.fetchall()
    conn.close()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)