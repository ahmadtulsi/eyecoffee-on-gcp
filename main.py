from flask import Flask, render_template, url_for, request, redirect

import os
import model
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

app = Flask(__name__, template_folder='Template')


# Log uploadedfile to Firestore
# cred = credentials.Certificate(
#     "eyecoffe-1aed99524ef7.json")
firebase_admin.initialize_app()
db = firestore.client()
eyecoffee_db = db.collection('eyecoffe')


@app.route('/', methods=['GET', 'POST'])
def index():
    now_timestamp = datetime.now()
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            image_path = os.path.join('static', uploaded_file.filename)
            uploaded_file.save(image_path)
            rs = model.get_prediction(image_path)
            result = {
                'class_name': rs["class_name"],
                'percentage': rs["percentage"],
                'image_path': image_path,
            }

            filename_data_save = image_path
            predict_class = rs["class_name"]
            percentage = rs["percentage"]

            eyecoffee_db.document().set({'percentage': percentage, 'predict_class': predict_class,
                                       'file_path': filename_data_save, 'timestamp': str(datetime.timestamp(now_timestamp))})
       
            return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)