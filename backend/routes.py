from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data),200

    return {"message": "Internal server error"}, 500    

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for i in data:
            if i.get("id") == id:
                return jsonify(i),200

    return {"message": "Not Found"}, 404    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_to_create = request.get_json()
    for i in data:
        if i.get('id') == picture_to_create.get('id'):
            return {"Message": f"picture with id {picture_to_create['id']} already present"},302

    data.append(picture_to_create)
    # json.dump(data, json_url)
    return jsonify(picture_to_create),201     

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_to_update = request.get_json()
    for i in data:
        if i.get('id') == picture_to_update.get('id'):
            for key in picture_to_update:
                i[key] = picture_to_update[key]
            return jsonify(i),200       
            
    return {"Message": f"picture not found"},404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in data:
        if i.get('id') == id:
            data.remove(i)
            return jsonify(id),204
                   
            
    return {"Message": f"picture not found"},404
