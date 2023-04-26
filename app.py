import os, ocrmypdf, tempfile
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

temp_directory_uploads = tempfile.TemporaryDirectory()
temp_directory_downloads = tempfile.TemporaryDirectory()

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = temp_directory_uploads.name
app.config['DOWNLOAD_FOLDER'] = temp_directory_downloads.name
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            for f in os.listdir(app.config['UPLOAD_FOLDER']):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


def process_file(path, filename):
    ocr_pdf(path, filename)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")

def ocr_pdf(path, filename):
    input_file = path
    for f in os.listdir(app.config['DOWNLOAD_FOLDER']):
        os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], f))
    output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    ocrmypdf.ocr(input_file, output_file, deskew=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
