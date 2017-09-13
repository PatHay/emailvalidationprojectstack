from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "SecretBox"
mysql = MySQLConnector(app,'emaildb')
@app.route('/')
def index():
    return render_template('index.html')  #pass data to our template

@app.route('/email_check', methods=['POST'])
def new_email():
    if len(request.form['email']) < 1:
        flash("Email is Blank!", "blank")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!", "invalid")
    else:
        session['entered_email'] = request.form['email']
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email': request.form['email']
            }
        mysql.query_db(query, data)
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def display():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails=emails)

app.run(debug=True)