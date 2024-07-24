import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, Blueprint, current_app
from flask_cors import cross_origin
from models import *

import logging
from file_runner import extensions, run_new_delete_old, readable_table
from ml_algos import set_column_name, distinct_type
from app.final_task import results
import base64


COLUMN_NAME = ""


bp = Blueprint("main", __name__)

logger = logging.getLogger(__name__)

# redis_conn = Redis()
# q = Queue(connection = redis_conn)

# @shared_task()

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
        print("task started")
        task = results.apply_async(args = [current_app.config["UPLOAD_FOLDER"], COLUMN_NAME])
        # job = q.enqueue(results)
       
        return jsonify({"task_id":task.id}), 202
        # return jsonify({"task_id":job.get_id()}), 202
    
    except Exception as e:
        logger.error(f"Error starting task: {e}", exc_info=True)
        return jsonify({"error":"Internal Server Error"})

@bp.route("/task-status/<task_id>", methods = ["GET"])
@cross_origin(origins = "http://localhost:3000")
def task_status(task_id):
    print("Waiting for work to happen...")
    task = results.AsyncResult(task_id)
    # task = q.fetch_job(task_id)
    # if task.is_finished:
    #     return jsonify({"status":"completed", "result":task.result})
    # elif task.is_failed:
    #     return jsonify({"status":"failed"})
    # else:
    #     return jsonify({"status":task.get_status()}), 200
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
    global COLUMN_NAME
    COLUMN_NAME = column_name
    print(column_name)
    set_column_name(column_name)
    # col_name = Column(column_name = column_name)
    # db.session.add(col_name)
    # db.session.commit()

    return jsonify({"message":"Column Name Successfully Added"}), 201


@bp.route("/column_name", methods = ["GET"])
def list_column_name():
    col_names = Column.query.all()
    return jsonify({"col_name": [{"col_name":col_name} for col_name in col_names]})



