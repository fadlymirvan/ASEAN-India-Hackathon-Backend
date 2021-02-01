from flask import request, json, Blueprint, Response, g
from ..models.DataModels import DataModels, DataSchema
from flask_jwt_extended import jwt_required

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
