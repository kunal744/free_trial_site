from flask import Flask, render_template, request, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(100))
    country = db.Column(db.String(50))

# Create tables
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Home page: form + download logic
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
            # Save user to database
            user = User(name=name, email=email, phone=phone, company=company, country=country)
            db.session.add(user)
            db.session.commit()

            # Show download link
            return render_template('index.html', download_ready=True)

    # Show form only
    return render_template('index.html', download_ready=False)

# Download route
@app.route('/download/<path:filename>')
def download(filename):
    safe_path = os.path.join(app.root_path, 'static', 'files')
    try:
        return send_from_directory(safe_path, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
