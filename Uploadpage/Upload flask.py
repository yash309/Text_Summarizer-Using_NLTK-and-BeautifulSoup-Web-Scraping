from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)
@app.route('/')
def upload_file():
    return render_template('Upload Form.html')
@app.route('/s',methods=["POST"])
def s():
    if request.method == 'POST':
       f = request.files['file']
       f.save(secure_filename(f.filename))
       return 'file uploaded successfully'
if __name__ == '__main__':
    app.run(debug=True,port=7000)