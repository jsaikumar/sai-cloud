from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(_name_)

# SQLite setup
BASE_DIR = os.path.dirname(os.path.abspath(_file_))  # Get the absolute directory
db_path = os.path.join(BASE_DIR, 'mydatabase.db')

conn = sqlite3.connect(db_path) #"/flaskapp/users.db
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))
@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

@app.route('/retrieve', methods = ['POST'])
def retrieve():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        #checking if the user exists in the database and to display the information
        return render_template('profile.html', user = user)
    else:
        #if the user does not exist, we return a message that the info is invalid
        return "Invalid username or password, please register or try again."
# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Check if the file is present in the request
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']

    # Check if the filename is empty
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file to the new uploads directory
    upload_directory = "/var/www/html/flaskapp"
    file_path = os.path.join(upload_directory, "uploaded_file.txt")
    file.save(file_path)

    # Calculate the word count in the uploaded file
    with open(file_path, "r") as f:
        content = f.read()
        word_count = len(content.split())

    return f"Uploaded file has {word_count} words."
  @app.route('/relogin')
def relogin():
    return render_template('relogin.html')

@app.route('/signin', methods = ['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        #checking if the user exists in the database and to display the information
        return render_template('profile.html', user = user)
    else:
        #if the user does not exist, we return a message that the info is invalid
        return "Invalid username or password, please register or try again."


if _name_ == '_main_':
    app.run(debug=True)
