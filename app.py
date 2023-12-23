from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_existing_files():
    return set(os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        existing_files = get_existing_files()
        files = request.files.getlist('files')
        uploaded_files = []

        for file in files:
            if file.filename == '':
                return render_template('upload.html', error='No selected file')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                if filename in existing_files:
                    continue  # Skip already existing files

                print(f"Saving file to: {filepath}")
                file.save(filepath)
                uploaded_files.append(filename)

        if uploaded_files:
            message = f"{len(uploaded_files)} files uploaded successfully: {', '.join(uploaded_files)}"
        else:
            message = "No new files uploaded. All files already exist in the directory."

        return render_template('upload.html', message=message)

    return render_template('upload.html', error=None)

@app.route('/document')
def document():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_size = os.path.getsize(filepath)
        file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024 else f"{file_size / (1024 * 1024):.2f} MB"
        files.append({'name': filename, 'size': file_size_str, 'type': filename.rsplit('.', 1)[1].lower()})

    return render_template('document.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about')
def about():
    return render_template('about.html')

# Define a custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Error handler for TemplateNotFound
@app.errorhandler(TemplateNotFound)
def template_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
