from flask import request, json, Blueprint, Response, send_file
from ..models.DataModels import DataModels, DataSchema
import csv
import io

data_api = Blueprint('data_api', __name__)
data_schema = DataSchema()


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
            "message": err
        }), status=400)

    data = DataModels(data)
    data.save()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Created Successfully!"
    }), status=201)


@data_api.route('/<int:data_id>', methods=['GET'])
def get_by_id(data_id):
    req = DataModels.get_data_by_id(data_id)
    if not req:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found"
        }), status=404)

    data = data_schema.dump(req)
    return Response(mimetype="application/json", response=json.dumps({
        "data": data
    }), status=200)


@data_api.route('/<int:data_id>', methods=['PUT'])
def update(data_id):
    req = request.get_json()
    data = DataModels.get_data_by_id(data_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found"
        }), status=404)

    try:
        data = data_schema.load(req, partial=True)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err
        }), status=400)

    data.update(data)
    data = data_schema.dump(data)
    return Response(mimetype="application/json", response=json.dumps({
        "message": "Updated Successfully",
        "data": data
    }), status=200)


@data_api.route('/<int:data_id>', methods=['DELETE'])
def delete(data_id):
    data = DataModels.get_data_by_id(data_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found"
        }), status=404)

    data.delete()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Deleted Successfully",
    }), status=200)


@data_api.route('/download', methods=['GET'])
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
