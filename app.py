from flask import Flask, render_template, request, redirect, url_for
import os
from summarizer import summarize_book

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to temporarily hold summary (auto-cleared on reload)
current_summary = ""

@app.route('/')
def index():
    global current_summary
    summary = current_summary
    current_summary = ""  # Clear after first render
    return render_template('index.html', summary=summary)

@app.route('/upload', methods=['POST'])
def upload():
    global current_summary
    file = request.files['file']
    language = request.form.get('language', 'English')

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        current_summary = summarize_book(file_path, language)
        return redirect(url_for('index'))

    return "File upload failed"

@app.route('/clear', methods=['POST'])
def clear():
    global current_summary
    current_summary = ""
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
