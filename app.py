from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for flash messages

# ✅ Updated path to match where your file actually is
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'statics', 'files')
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    download_ready = False

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        country = request.form.get('country')
        agree = request.form.get('agree')

        # Basic validation
        if not name or not email or not country or not agree:
            flash("Please complete all required fields.", "error")
        else:
            download_ready = True

    return render_template('index.html', download_ready=download_ready)

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        flash("File not found.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
