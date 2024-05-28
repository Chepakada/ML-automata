from app import create_app, db
from flask import Flask, jsonify, request
from models import *
import os
app = create_app()

@app.route("/files", methods = ["POST"])
def upload_files():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No Selected File"}), 400
    
    if file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        new_file = Files(filename = file.filename, filepath = file_path)

        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message":"File successfully uploaded", "file_path": file_path})
    

@app.route("/files", methods = ["GET"])
def list_files():
    files = Files.query.all()
    return jsonify({"files":[{"filename":file.filename, "filepath":file.filepath} for file in files]})

@app.route("/files/<filename>", methods = ["GET"])
def get_file(filename):

    file = Files.query.filter_by(filename = filename)
    if file:
        return jsonify

if __name__ == "__main__":
    app.run(debug=True)
