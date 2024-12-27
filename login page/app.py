from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = '468e244df5c54c3b180f34f0129fb879'

#database function
def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL,
                   email TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()


init_db()
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =="POST":
        username=request.form['username']
        password=request.form['password']


        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",(username,))
        user = cursor.fetchone()
        conn.close()


        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            flash("Login Successful!", "succes")
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password","danger")
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        hashed_password= generate_password_hash(password, method='pbkdf2:sha256')

        try:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",
            (username, hashed_password, email))

            conn.commit()
            conn.close()
            flash("Registration successfull! you can now log in.","success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("username or email already exists","danger")

    return render_template('registration.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', name=session['username'], msg="login Successful")

    else:
        flash("Please log in to access this page", "danger")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("You have benn logged out","info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)






        

    