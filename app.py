from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/enter-new')
def new_student():
    return render_template('new-student.html')

@app.route('/add-student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        try:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            phone_number = request.form['phone_number']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, address, city, phone_number) VALUES (?,?,?,?)", (name, address, city, phone_number))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/list-students')
def list_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    return render_template("list-students.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
