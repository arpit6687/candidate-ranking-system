from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_candidate():

    if request.method == 'POST':

        name = request.form['name']
        cgpa = request.form['cgpa']
        aptitude = request.form['aptitude']
        technical = request.form['technical']
        interview = request.form['interview']

        final_score = (
            float(cgpa) * 10 +
            int(aptitude) +
            int(technical) +
            int(interview)
        )

        connection = sqlite3.connect('database.db')

        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO candidates
        (name, cgpa, aptitude, technical, interview, final_score)

        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, cgpa, aptitude, technical, interview, final_score))

        connection.commit()

        connection.close()

        return "Candidate Added Successfully"

    return render_template('add_candidate.html')

@app.route('/ranking')
def ranking():

    search = request.args.get('search')

    connection = sqlite3.connect('database.db')

    cursor = connection.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM candidates
        WHERE name LIKE ?
        ORDER BY final_score DESC
        """, ('%' + search + '%',))

    else:

        cursor.execute("""
        SELECT * FROM candidates
        ORDER BY final_score DESC
        """)

    candidates = cursor.fetchall()

    connection.close()

    return render_template('ranking.html', candidates=candidates)

@app.route('/delete/<int:id>')
def delete_candidate(id):

    connection = sqlite3.connect('database.db')

    cursor = connection.cursor()

    cursor.execute("DELETE FROM candidates WHERE id = ?", (id,))

    connection.commit()

    connection.close()

    return redirect('/ranking')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_candidate(id):

    connection = sqlite3.connect('database.db')

    cursor = connection.cursor()

    if request.method == 'POST':

        cgpa = request.form['cgpa']
        aptitude = request.form['aptitude']
        technical = request.form['technical']
        interview = request.form['interview']

        final_score = (
            float(cgpa) * 10 +
            int(aptitude) +
            int(technical) +
            int(interview)
        )

        cursor.execute("""
        UPDATE candidates
        SET cgpa=?, aptitude=?, technical=?, interview=?, final_score=?
        WHERE id=?
        """, (cgpa, aptitude, technical, interview, final_score, id))

        connection.commit()

        connection.close()

        return redirect('/ranking')

    cursor.execute("SELECT * FROM candidates WHERE id=?", (id,))

    candidate = cursor.fetchone()

    connection.close()

    return render_template('edit_candidate.html', candidate=candidate)
if __name__ == '__main__':
    app.run(debug=True)