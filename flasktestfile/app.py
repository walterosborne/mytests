from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            data = file.read()
            df = pd.read_excel(BytesIO(data))
            return df.to_html()  # You can customize how you want to display the data
        else:
            return 'Invalid file format. Please upload an Excel file.'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
