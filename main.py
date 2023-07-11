from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)

app.secret_key = 'the random string'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'tiff', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ProcessImg(filename, operation):
    print(f"Operation is {operation} and filename is {filename}")
    image = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            procImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/{filename}", procImg)
            return procImg
        case 'cpng':
            new = f'static/{filename.split(".")[0]}.png'
            cv2.imwrite(new,image)
            return new
        case 'cjpg':
             new = f'static/{filename.split(".")[0]}.jpg'
             cv2.imwrite(new,image)
             return new

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/edit', methods= ['GET', 'POST'])
def edit():
    if request.method == 'POST':
            operation = request.form.get('operation')
        # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return "error"
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return "No filename found!"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new = ProcessImg(filename, operation)
                flash(f"Your image is processed and is available <a href='/{new}' target='_blank'> here </a>")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug= True)
