from flask import request, json, Blueprint, Response, send_file
from werkzeug.utils import secure_filename
from ..models.DataModels import DataModels, DataSchema
import csv
import os

data_api = Blueprint('data_api', __name__)
data_schema = DataSchema()

ALLOWED_EXTENSIONS = {'txt', 'csv', 'json'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@data_api.route('/', methods=['GET'])
def get_all():
    req = DataModels.get_all_data()
    data = data_schema.dump(req, many=True)

    return Response(mimetype="application/json", response=json.dumps({
        "data": data
    }), status=200)


@data_api.route('/', methods=['POST'])
def create():
    req = request.get_json()
    try:
        data = data_schema.load(req)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err,
            "status": 400,
        }), status=400)

    data = DataModels(data)
    data.save()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Created Successfully!",
        "status": 201,
    }), status=201)


@data_api.route('/<int:data_id>', methods=['GET'])
def get_by_id(data_id):
    req = DataModels.get_data_by_id(data_id)
    if not req:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404,
        }), status=404)

    data = data_schema.dump(req)
    return Response(mimetype="application/json", response=json.dumps({
        "data": data,
        "status": 200,
    }), status=200)


@data_api.route('/<int:data_id>', methods=['PUT'])
def update(data_id):
    req = request.get_json()
    data = DataModels.get_data_by_id(data_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404,
        }), status=404)

    try:
        data = data_schema.load(req, partial=True)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err,
            "status": 400,
        }), status=400)

    data.update(data)
    data = data_schema.dump(data)
    return Response(mimetype="application/json", response=json.dumps({
        "message": "Updated Successfully",
        "status": 200,
        "data": data
    }), status=200)


@data_api.route('/<int:data_id>', methods=['DELETE'])
def delete(data_id):
    data = DataModels.get_data_by_id(data_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404,
        }), status=404)

    data.delete()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Deleted Successfully",
        "status": 200,
    }), status=200)


@data_api.route('/csv/download', methods=['GET'])
def generate_csv():
    file = 'D:/Project/ASEAN-IndiaHackathon/backend/static/csv/fishing_data.csv'
    with open(file, 'w') as csvfile:
        output_csv = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        headers = [
            'date',
            'lat_bin',
            'long_bin',
            'mmsi',
            'fishing_hours'
        ]

        db_headers = [
            'created_at',
            'lat',
            'long',
            'frequency',
            'fishing_hours'
        ]

        output_csv.writerow(headers)

        for record in DataModels.get_all_data():
            output_csv.writerow([getattr(record, c) for c in db_headers])

    return send_file(file, mimetype="text/csv",
                     attachment_filename='fishing_data.csv',
                     as_attachment=True)


@data_api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "No File Part in the Request!",
            "status": 400,
        }), status=400)

    file = request.files['file']

    if file.filename == '':
        return Response(mimetype="application/json", response=json.dumps({
            "message": "No File Selected for Uploading",
            "status": 400,
        }), status=400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getenv('UPLOAD_FOLDER'), filename))
        return Response(mimetype="application/json", response=json.dumps({
            "message": "File Successfully Uploaded",
            "status": 201,
        }), status=201)

    else:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "File Types are not Allowed! Allowed File type ('txt', 'csv', 'json')",
            "status": 400,
        }), status=400)
