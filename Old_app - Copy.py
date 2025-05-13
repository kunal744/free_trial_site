from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(100))
    country = db.Column(db.String(50))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        company = request.form.get('company', '')
        country = request.form['country']
        agree = request.form.get('agree')

        if name and email and country and agree:
            user = User(name=name, email=email, phone=phone, company=company, country=country)
            db.session.add(user)
            db.session.commit()
            return render_template('index.html', download_ready=True)

    return render_template('index.html', download_ready=False)

if __name__ == '__main__':
    app.run(debug=True)
