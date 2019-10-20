from flask import Flask, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import os.path
from whoosh.index import create_in, open_dir

# index engine setup title of package, blob_url for Gcloud Storage, 
schema = Schema(title=TEXT(stored=True),
                blob_url=TEXT,
                path=ID(stored=True),
                tags=KEYWORD)

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)

ix = open_dir("index")

# upload folder temporarily might delete later in place of gcloud
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pickle'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# will post to gcloud soon
@application.route("/upload", methods=['GET', 'POST'])
def upload_file():
    # todo: push to gcloud and return URL
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            return redirect("/")
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect("/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect('/upload')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@application.route("/add-to-index", methods=['POST'])
def add_to_index():
    # todo: add url to blob store and name of pkg to whoosh
    pass


@application.route("/search-the-index", methods=['GET'])
def search_the_index():
    # todo: query whoosh indexing engine
    pass


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    application.run(host='0.0.0.0')