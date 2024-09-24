import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the homepage where the form is located
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and form submission
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    config_type = request.form.get('config_type')

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Call the script to process the CSV and push configurations using Ansible
        try:
            subprocess.run(['python3', 'generate_configs.py', filepath, config_type], check=True)
            flash('Configuration successfully pushed to routers')
        except subprocess.CalledProcessError as e:
            flash(f'Error pushing configurations: {e}')
        return redirect(url_for('index'))
    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)

