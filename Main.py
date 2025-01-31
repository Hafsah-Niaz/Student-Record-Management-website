from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'sahhaf25'    # Your MySQL password
app.config['MYSQL_DB'] = 'student_db'      # Change to your database name

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        class_name = request.form['class']
        phone = request.form['phone']
        age = request.form['age']
        course = request.form['course']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(name, email, dob, class, phone, age, course) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (name, email, dob, class_name, phone, age, course))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/edit_student/<id>', methods=['GET', 'POST'])
def edit_student(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        class_name = request.form['class']  # Updated to 'class'
        phone = request.form['phone']
        age = request.form['age']
        course = request.form['course']

        cur.execute("UPDATE students SET name=%s, email=%s, dob=%s, class=%s, phone=%s, age=%s, course=%s WHERE id=%s", 
                    (name, email, dob, class_name, phone, age, course, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()
    return render_template('edit.html', student=student)

@app.route('/delete_student/<id>', methods=['GET'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


