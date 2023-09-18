import os
from flask import Flask, request, render_template, send_file, abort

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return index()

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/preview_file/<filename>')
def preview_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        # Check if the file is a text file
        if filename.lower().endswith(('.txt', '.log', '.md', '.py','.doc','docx')):
            with open(file_path, 'r') as file:
                content = file.read()
            return content, 200, {'Content-Type': 'text/plain'}
        else:
            return send_file(file_path)
    else:
        abort(404)
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False

# Route to handle file deletion
@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete(filename):
    if request.method == 'POST':
        if delete_file(filename):
            return index()
        else:
            return index()
    return render_template('index.html', filename=filename)
    
if __name__ == '__main__':
    app.run(debug=True)
