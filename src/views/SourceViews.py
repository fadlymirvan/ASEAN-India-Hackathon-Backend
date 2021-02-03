from flask import request, json, Blueprint, Response, g
from ..models.SourceModels import SourceModels, SourceSchema
from flask_jwt_extended import jwt_required

source_api = Blueprint('source_api', __name__)
source_schema = SourceSchema()


@source_api.route('/', methods=['GET'])
def get_all():
    req = SourceModels.get_all_source()
    data = source_schema.dump(req, many=True)

    return Response(mimetype="application/json", response=json.dumps({
        "data": data,
        "status": 200
    }), status=200)


@source_api.route('/', methods=['POST'])
def create():
    req = request.get_json()
    try:
        data = source_schema.load(req)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err,
            "status": 400
        }), status=400)

    data = SourceModels(data)
    data.save()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Created Successfully!",
        "status": 201
    }), status=201)


@source_api.route('/<int:source_id>', methods=['GET'])
def get_by_id(source_id):
    req = SourceModels.get_source_by_id(source_id)
    if not req:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404
        }), status=404)

    data = source_schema.dump(req)
    return Response(mimetype="application/json", response=json.dumps({
        "data": data,
        "status": 200
    }), status=200)


@source_api.route('/<int:source_id>', methods=['PUT'])
def update(source_id):
    req = request.get_json()
    data = SourceModels.get_source_by_id(source_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404
        }), status=404)

    try:
        data = source_schema.load(req, partial=True)

    except Exception as err:
        return Response(mimetype="application/json", response=json.dumps({
            "message": err,
            "status": 400
        }), status=400)

    data.update(data)
    data = source_schema.dump(data)
    return Response(mimetype="application/json", response=json.dumps({
        "message": "Updated Successfully",
        "data": data,
        "status": 200
    }), status=200)


@source_api.route('/<int:source_id>', methods=['DELETE'])
def delete(source_id):
    data = SourceModels.get_source_by_id(source_id)
    if not data:
        return Response(mimetype="application/json", response=json.dumps({
            "message": "Data Not Found",
            "status": 404
        }), status=404)

    data.delete()

    return Response(mimetype="application/json", response=json.dumps({
        "message": "Deleted Successfully",
        "status": 200
    }), status=200)
