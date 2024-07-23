from app import app
from flask import Flask, jsonify, request, Blueprint, current_app
from flask_cors import cross_origin
from models import *
import os
from flask import jsonify
import base64
from celery import shared_task
import logging

from file_runner import extensions, run_new_delete_old, readable_table
from ml_algos import set_column_name, distinct_type

bp = Blueprint("main", __name__)

logger = logging.getLogger(__name__)

@shared_task()
def results(file_path):
    try:
        file = run_new_delete_old(file_path)
        
        table = readable_table(file)
        output = distinct_type(table)
        if output[0] == "RNN":
            return jsonify({"type": output[0], "output": output[1], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
        if output[0] == "classification":
            return jsonify({"type": output[0], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
        if output[0] == "linear_reg":
            return jsonify({"type": output[0], "metrics":output[2],"images": {"metric_image":base64.b64encode(output[3].getvalue()).decode('utf-8'), "scatter_image":base64.b64encode(output[4].getvalue()).decode('utf-8') }})  
    except Exception as e:
        raise e 

@bp.route("/files", methods = ["POST"])
def upload_files():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No Selected File"}), 400
    
    _, file_ext = file.filename.split(".", 1)

    if file_ext not in extensions:
        return jsonify({"error": "The file extension is not supported"}), 403
    
    if file:
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        # new_file = Files(filename = file.filename, filepath = file_path)
        

        # db.session.add(new_file)
        # db.session.commit()
        return jsonify({"message":"File successfully uploaded", "file_path": file_path})
    
@bp.route("/start-task", methods = ["POST"])
@cross_origin(origins="http://localhost:3000")
def start_task():
    try:
        task = results.apply_async(args = [current_app.config["UPLOAD_FOLDER"]])
        print("  \n \n \n")
        print(task.id)
        print("  \n \n \n")
        return jsonify({"task_id":task.id}), 202
    
    except Exception as e:
        logger.error(f"Error starting task: {e}", exc_info=True)
        return jsonify({"error":"Internal Server Error"})

@bp.route("/task-status/<task_id>", methods = ["GET"])
@cross_origin(origins = "http://localhost:3000")
def task_status(task_id):
    task = results.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state":task.state,
            "status":"Pending......"
        }
    elif task.state == "STARTED":
        response = {
            "state":task.state,
            "status":"Task is in progress......"
        }
    elif task.state == "SUCCESS":
        response = {
            "state":task.state,
            "result":task.info
        }
    else:
        response = {
            "state":task.state,
            "status":str(task.info)
        }
    return jsonify(response)

@bp.route("/files", methods = ["GET"])
def list_files():
    files = Files.query.all()
    return jsonify({"files":[{"filename":file.filename, "filepath":file.filepath} for file in files]})

@bp.route("/files/<filename>", methods = ["GET"])
def get_file(filename):

    file = Files.query.filter_by(filename = filename)
    if file:
        return jsonify
    
### Below this is for the column name ###

@bp.route("/column_name", methods = ["POST"])
def create_col_name():
    data = request.get_json()
    column_name = data.get("data")
    set_column_name(column_name)
    # col_name = Column(column_name = column_name)
    # db.session.add(col_name)
    # db.session.commit()

    return jsonify({"message":"Column Name Successfully Added"}), 201


@bp.route("/column_name", methods = ["GET"])
def list_column_name():
    col_names = Column.query.all()
    return jsonify({"col_name": [{"col_name":col_name} for col_name in col_names]})



if __name__ == "__main__":
    app.run(debug=True,  host='127.0.0.1', port=5000)


