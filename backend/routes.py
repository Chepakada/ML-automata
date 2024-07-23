from app import create_app, db
from flask import Flask, jsonify, request
from models import *
import os
import io
import base64
from file_runner import extensions, run_new_delete_old, readable_table
from ml_algos import set_column_name, distinct_type


app = create_app()


@app.route("/files", methods = ["POST"])
def upload_files():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No Selected File"}), 400
    
    _, file_ext = file.filename.split(".", 1)

    if file_ext in extensions:
        return jsonify({"error": "The file extension is not supported"}), 403
    
    if file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        new_file = Files(filename = file.filename, filepath = file_path)
        

        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message":"File successfully uploaded", "file_path": file_path})
    
@app.route("/results", methods = ["GET"])
def results():
    file = run_new_delete_old(app.config["UPLOAD_FOLDER"])
    output = readable_table(file)
    if output[0] == "RNN":
        return jsonify({"type": output[0], "output": output[1], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
    if output[0] == "classification":
        return jsonify({"type": output[0], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
    if output[0] == "linear_reg":
        return jsonify({"type": output[0], "metrics":output[2],"images": {"metric_image":base64.b64encode(output[3].getvalue()).decode('utf-8'), "scatter_image":base64.b64encode(output[4].getvalue()).decode('utf-8') }})  



@app.route("/files", methods = ["GET"])
def list_files():
    files = Files.query.all()
    return jsonify({"files":[{"filename":file.filename, "filepath":file.filepath} for file in files]})

@app.route("/files/<filename>", methods = ["GET"])
def get_file(filename):

    file = Files.query.filter_by(filename = filename)
    if file:
        return jsonify
    
### Below this is for the column name ###

@app.route("/column_name", methods = ["POST"])
def create_col_name():
    data = request.get_json()
    column_name = data.get("data")
    set_column_name(column_name)
    col_name = Column(column_name = column_name)
    db.session.add(col_name)
    db.session.commit()

    return jsonify({"message":"Column Name Successfully Added"}), 201


@app.route("/column_name", methods = ["GET"])
def list_column_name():
    col_names = Column.query.all()
    return jsonify({"col_name": [{"col_name":col_name} for col_name in col_names]})



if __name__ == "__main__":
    app.run(debug=True,  host='127.0.0.1', port=5000)
