from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'crm-secret-key')

app.config['MYSQL_HOST']     = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER']     = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB']       = os.environ.get('MYSQL_DB', 'employee_crm')

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        emp_code = request.form['emp_code']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employees WHERE emp_code=%s AND password=%s",
                    (emp_code, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user'] = user[1]
            return redirect('/employees')
        error = 'Invalid Employee Code or Password!'
    return render_template('login.html', error=error)

@app.route('/employees')
def employees():
    if 'user' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()
    return render_template('employees.html', employees=data)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name     = request.form['name']
        emp_code = request.form['emp_code']
        password = request.form['password']
        dept     = request.form['department']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees(name, emp_code, password, department) VALUES(%s,%s,%s,%s)",
                    (name, emp_code, password, dept))
        mysql.connection.commit()
        cur.close()
        return redirect('/employees')
    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if 'user' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['department']
        cur.execute("UPDATE employees SET name=%s, department=%s WHERE id=%s",
                    (name, dept, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/employees')
    cur.execute("SELECT * FROM employees WHERE id=%s", (id,))
    emp = cur.fetchone()
    cur.close()
    return render_template('edit_employee.html', emp=emp)

@app.route('/delete/<int:id>')
def delete_employee(id):
    if 'user' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/employees')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)