from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

port = 8888



storage_dir = 'files/'

if not os.path.exists(storage_dir):
    os.makedirs(storage_dir)


@app.route('/upload/<document_id>', methods=['POST'])
def upload_file(document_id:str):
    # Read the zipped data from the body of the request
    zipped_data = request.data
    if not zipped_data:
        return 'No data in request', 400
    filename = secure_filename(f'{document_id}.zip')
    with open(os.path.join(storage_dir, filename), 'wb') as f:
        f.write(zipped_data)
    return {'success':True}, 200

@app.route('/download/<document_id>', methods=['GET'])
def download_file(document_id:str):
    filename = secure_filename(f'{document_id}.zip')
    file_path = os.path.join(storage_dir, filename)
    if not os.path.isfile(file_path):
        return 'File not found', 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=port)